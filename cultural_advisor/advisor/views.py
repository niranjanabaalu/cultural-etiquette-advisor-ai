import json
import logging
import traceback
import time
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ChatSession, ChatMessage, Etiquette
from .nlp_engine import detect_intent, extract_location
from .gemini_service import get_gemini_response_with_retry

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def chatbot(request):
    """
    API-driven chatbot with NVIDIA NIM integration and conversation persistence.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)
        message = body.get("message", "").strip()
        session_id = body.get("session_id")

        if not message:
            return JsonResponse({"error": "Empty message"}, status=400)

        # 1. Detect location (Current query or Session)
        current_location = extract_location(message)
        session_location = request.session.get('last_location')
        
        # Use current location if found, otherwise fallback to session
        active_location = current_location if current_location else session_location
        
        # Update session if a new location is found
        if current_location:
            request.session['last_location'] = current_location
            request.session.modified = True

        # 2. Build Cultural Context from Database
        db_context = ""
        if active_location:
            etiquette = Etiquette.objects.filter(country__iexact=active_location).first()
            if etiquette:
                sections = []
                if etiquette.greeting_word: sections.append(f"Greetings: {etiquette.greeting_word}")
                if etiquette.dining_etiquette: sections.append(f"Dining: {etiquette.dining_etiquette}")
                if etiquette.business_meeting: sections.append(f"Business: {etiquette.business_meeting}")
                if etiquette.dress_code: sections.append(f"Dress Code: {etiquette.dress_code}")
                context_str = " | ".join(sections[:5])
                db_context = f"Expert Database Info for {active_location}: {context_str}"

        # 3. Comprehensive Logging
        intent = detect_intent(message)
        print(f"\n[DEBUG] --- Chatbot Request ---")
        print(f"[DEBUG] Message: {message}")
        print(f"[DEBUG] Intent: {intent}")
        print(f"[DEBUG] Detected Location: {current_location}")
        print(f"[DEBUG] Session Location: {session_location}")
        print(f"[DEBUG] Active Location: {active_location}")
        print(f"[DEBUG] -----------------------\n")

        # 4. Construct Structured Prompt
        if active_location:
            final_prompt = (
                f"CONTEXT: The user is asking about {active_location}.\n"
                f"{db_context}\n\n"
                f"USER MESSAGE: {message}"
            )
        else:
            final_prompt = message

        session = None
        if session_id:
            session = ChatSession.objects.filter(id=session_id, user=request.user).first()

        if not session:
            session = ChatSession.objects.create(user=request.user, title=message[:30] + "...")

        ChatMessage.objects.create(session=session, is_bot=False, content=message)

        # 5. Get AI Response
        reply = get_gemini_response_with_retry(final_prompt)
        
        ChatMessage.objects.create(session=session, is_bot=True, content=reply)
        session.save()

        return JsonResponse({
            "reply": reply, 
            "session_id": session.id,
            "detected_location": active_location
        })

    except Exception as e:
        logger.error(f"Chatbot View Error: {e}\n{traceback.format_exc()}")
        return JsonResponse({'reply': "I hit a minor glitch! Could you ask your question again?"}, status=500)

# ---------------------------
# AUTH VIEWS AND HOME
# ---------------------------

def signup_view(request):
    if request.method == "POST":
        from django.contrib.auth.forms import UserCreationForm
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import login
            login(request, user)
            return redirect('home')
    else:
        from django.contrib.auth.forms import UserCreationForm
        form = UserCreationForm()
    return render(request, "advisor/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        from django.contrib.auth.forms import AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            from django.contrib.auth import login
            login(request, user)
            return redirect('home')
    else:
        from django.contrib.auth.forms import AuthenticationForm
        form = AuthenticationForm()
    return render(request, "advisor/login.html", {"form": form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

@login_required
def reset_context(request):
    """
    Clears the cultural context memory for a new session.
    """
    if 'last_location' in request.session:
        del request.session['last_location']
    return JsonResponse({"status": "context reset"})


@login_required
def home(request):
    return render(request, "advisor/index.html")

# HISTORY VIEWS (Remained same)
@login_required
def get_chat_history(request):
    sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    history = [{"id": s.id, "title": s.title, "timestamp": s.updated_at.strftime("%b %d, %H:%M")} for s in sessions]
    return JsonResponse({"history": history})

@login_required
def get_session_messages(request, session_id):
    session = ChatSession.objects.filter(id=session_id, user=request.user).first()
    if not session:
        return JsonResponse({"error": "Session not found"}, status=404)
    messages = session.messages.all().order_by('timestamp')
    data = [{"is_bot": m.is_bot, "content": m.content, "timestamp": m.timestamp.strftime("%H:%M")} for m in messages]
    return JsonResponse({"messages": data})

@login_required
def delete_chat_session(request, session_id):
    ChatSession.objects.filter(id=session_id, user=request.user).delete()
    return JsonResponse({"status": "deleted"})