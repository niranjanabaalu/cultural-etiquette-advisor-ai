from django.contrib import admin
from .models import Etiquette, ChatSession, ChatMessage, APILog

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'is_success', 'latency', 'timestamp')
    list_filter = ('api_name', 'is_success', 'timestamp')
    readonly_fields = ('api_name', 'endpoint', 'query', 'is_success', 'latency', 'timestamp')

@admin.register(Etiquette)
class EtiquetteAdmin(admin.ModelAdmin):
    list_display = ('country', 'region', 'continent', 'capital_city', 'created_at')
    search_fields = ('country', 'region', 'continent')
    list_filter = ('continent', 'region')
    fieldsets = (
        ('Basic Information', {
            'fields': ('country', 'region', 'continent', 'capital_city', 'official_name', 'flag_url', 'currency', 'population')
        }),
        ('Greetings & Communication', {
            'fields': ('greeting_word', 'greeting_gesture', 'communication_style', 'communication_tips')
        }),
        ('Dining & Food', {
            'fields': ('dining_etiquette', 'table_manners', 'traditional_food', 'eating_style')
        }),
        ('Social Norms', {
            'fields': ('dress_code', 'marriage_dress', 'festival_culture', 'famous_festivals', 'public_behavior')
        }),
        ('Business & Education', {
            'fields': ('business_meeting', 'education_dress', 'gift_giving', 'gift_culture_specific')
        }),
        ('Advice & Tourism', {
            'fields': ('dos', 'donts', 'tourist_tips')
        }),
    )

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    search_fields = ('user__username', 'title')
    list_filter = ('created_at',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'is_bot', 'content_preview', 'timestamp')
    list_filter = ('is_bot', 'timestamp')
    
    def content_preview(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")