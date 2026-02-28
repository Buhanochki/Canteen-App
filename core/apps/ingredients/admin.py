from django.contrib import admin

from core.apps.ingredients.models import Ingredient


@admin.register(Ingredient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "amount",
        "created_at",
        "updated_at",
    )