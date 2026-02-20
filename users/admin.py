from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "telegram_chat_id", "is_staff", "is_active")
    search_fields = ("username", "telegram_chat_id")
