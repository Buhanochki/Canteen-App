from django.contrib import admin

from core.apps.meals.models import Meal, UserMeal, Day

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "day",
        "cost",
        "category",
        "created_at",
        "updated_at",
    )


@admin.register(UserMeal)
class UserMealAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "meal",
        "is_given",
        "created_at",
        "updated_at"
    )


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "date",
        "created_at",
        "updated_at"
    )





