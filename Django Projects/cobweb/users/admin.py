from django.contrib import admin
from .models import Profile, ChatMessage, Friend

admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(ChatMessage)