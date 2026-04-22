from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chatbot, name='chat'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.get_chat_history, name='get_chat_history'),
    path('messages/<int:session_id>/', views.get_session_messages, name='get_session_messages'),
    path('delete-session/<int:session_id>/', views.delete_chat_session, name='delete_chat_session'),
    path('reset-context/', views.reset_context, name='reset_context'),
]