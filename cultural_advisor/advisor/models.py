from django.db import models
from django.contrib.auth.models import User

class Etiquette(models.Model):

    country = models.CharField(max_length=100, db_index=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    continent = models.CharField(max_length=50, blank=True, null=True)
    capital_city = models.CharField(max_length=100, blank=True, null=True)

    # Greeting Culture
    greeting_word = models.CharField(max_length=100, blank=True, null=True)
    greeting_gesture = models.TextField(blank=True, null=True)

    # Communication
    communication_style = models.TextField(blank=True, null=True)
    communication_tips = models.TextField(blank=True, null=True)

    # Dining
    dining_etiquette = models.TextField(blank=True, null=True)
    table_manners = models.TextField(blank=True, null=True)

    # Dress
    dress_code = models.TextField(blank=True, null=True)

    # Gift culture
    gift_giving = models.TextField(blank=True, null=True)

    # Public behavior
    public_behavior = models.TextField(blank=True, null=True)

    # Business etiquette
    business_meeting = models.TextField(blank=True, null=True)

    # Language info
    language = models.CharField(max_length=100, blank=True, null=True)
    basic_words = models.TextField(blank=True, null=True)
    pronunciation = models.TextField(blank=True, null=True)

    # Advice
    dos = models.TextField(blank=True, null=True)
    donts = models.TextField(blank=True, null=True)

    # Tourism
    tourist_tips = models.TextField(blank=True, null=True)

    # NEW: Expanded Cultural Categories
    marriage_dress = models.TextField(blank=True, null=True)
    festival_culture = models.TextField(blank=True, null=True)
    famous_festivals = models.TextField(blank=True, null=True)
    traditional_food = models.TextField(blank=True, null=True)
    eating_style = models.TextField(blank=True, null=True)
    education_dress = models.TextField(blank=True, null=True)
    gift_culture_specific = models.TextField(blank=True, null=True)

    # API Caching / Auxiliary Fields
    flag_url = models.URLField(max_length=255, blank=True, null=True)
    official_name = models.CharField(max_length=200, blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.country

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Refactor fields for optimization
    flag_sent = models.BooleanField(default=False)
    last_country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    is_bot = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        role = "Bot" if self.is_bot else "User"
        return f"{role}: {self.content[:50]}"

class APILog(models.Model):
    """
    Tracks external API calls (Gemini, REST Countries, Wikipedia) for monitoring and debugging.
    """
    API_CHOICES = (
        ('GEMINI', 'Google Gemini AI'),
        ('REST_COUNTRIES', 'REST Countries API'),
        ('WIKIPEDIA', 'Wikipedia'),
    )
    
    api_name = models.CharField(max_length=50, choices=API_CHOICES)
    endpoint = models.CharField(max_length=255)
    query = models.TextField(null=True, blank=True)
    is_success = models.BooleanField(default=True)
    latency = models.FloatField(help_text="Response time in seconds", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.api_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name_plural = "API Logs"