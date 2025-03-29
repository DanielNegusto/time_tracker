from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_moderator",
    )  # Поля, которые вы хотите отображать в списке пользователей
    list_filter = ("is_staff", "is_moderator")  # Фильтры в админке
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_moderator",)}),  # Добавляем поле is_moderator
    )


admin.site.register(User, CustomUserAdmin)
