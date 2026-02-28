from django.db import models
from core.apps.common.models import TimedBaseModel
from core.apps.users.models import CustomUser
from core.apps.ingredients.models import Ingredient

class MealReport(TimedBaseModel):
    date = models.DateField(
        verbose_name="Дата создания репорта",
        auto_now=True,
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Пользователь",
        related_name="meal_report",
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиент",
        on_delete=models.CASCADE,
        related_name="meal_report",
    )
    amount = models.IntegerField(
        verbose_name="Количество потраченнных"
    )

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ['pk']