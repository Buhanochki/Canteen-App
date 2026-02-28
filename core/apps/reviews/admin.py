from django.contrib import admin

from core.apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "meal",
        "rate",
        "created_at",
        "updated_at"
    )

