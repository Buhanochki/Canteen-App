from django.contrib import admin
from core.apps.reports.models import MealReport

@admin.register(MealReport)
class AdminMealReport(admin.ModelAdmin):
    list_display = [
        'date',
        'user',
        'ingredient',
        'amount',
    ]