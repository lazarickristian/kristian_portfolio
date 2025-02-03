from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')  # Add created_at here
    list_filter = ('created_at',)  # Optional: Adds a filter by date