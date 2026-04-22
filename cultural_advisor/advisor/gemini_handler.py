import time
import logging
from google import genai
from django.conf import settings
from .models import APILog
logger = logging.getLogger(__name__)
# GLOBAL API CLIENT (Created only once)
gemini_client = None
if settings.GOOGLE_API_KEY:
    try:
        gemini_client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Gemini Client: {e}")
def get_gemini_response(prompt, context_data=None):
    """
    Sends a prompt to the Google Gemini API (Single call, optimized).
    """
    if not gemini_client:
        return "Please add your GOOGLE_API_KEY to the .env file to enable AI responses!"
    model_id = getattr(settings, 'GEMINI_MODEL_NAME', 'models/gemini-2.0-flash')
    
    system_instructions = (
        "You are a professional Cultural Etiquette Advisor. "
        "Keep responses very natural, brief, in conversational English, and limit to 3-5 sentences maximum. "
        "Never dump raw fields."
    )
    
    full_prompt = f"Instruction: {system_instructions}\n"
    if context_data:
        full_prompt += f"Background Context: {context_data}\n"
    full_prompt += f"Question: {prompt}"
    start_time = time.time()
    
    try:
        # SINGLE CALL ONLY - No inner retries
        response = gemini_client.models.generate_content(model=model_id, contents=full_prompt)
        
        latency = time.time() - start_time
        if response and response.text:
            APILog.objects.create(api_name='GEMINI', endpoint=model_id, query=prompt[:255], is_success=True, latency=latency)
            return response.text.strip()
            
    except Exception as e:
        latency = time.time() - start_time
        err_msg = str(e)
        logger.error(f"Gemini API Error: {err_msg}")
        APILog.objects.create(api_name='GEMINI', endpoint=model_id, is_success=False, latency=latency)
        # EXACT Rate Limit / Resource Exhausted Handling
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            return "I'm a bit busy fetching new information. Please try again in a few seconds 😊"
            
        return "I hit a minor connection issue. Please try asking again in a moment."
    return "I'm a bit busy fetching new information. Please try again in a few seconds 😊"
