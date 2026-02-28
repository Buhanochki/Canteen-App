from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "status",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Основная информация",
            {
                "classes": ("wide",),
                "fields": (
                    "last_name",
                    "first_name",
                    "surname",
                    "email",
                    "status",
                    "allergies"
                ),
            },
        ),
        (
            "Пароль",
            {
                "classes": ("wide",),
                "fields": ("password",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "last_name",
                    "first_name",
                    "surname",
                    "status",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    ordering = ["id"]
