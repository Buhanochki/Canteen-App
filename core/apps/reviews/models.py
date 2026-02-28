from django.db import models
from core.apps.common.models import TimedBaseModel
from core.apps.users.models import CustomUser
from core.apps.meals.models import Meal


class Review(TimedBaseModel):
    text = models.TextField(
        verbose_name="Текст отзыва"
    )

    user = models.ForeignKey(
        CustomUser,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="review"
    )
    meal = models.ForeignKey(
        Meal, 
        verbose_name="Блюдо",
        on_delete=models.CASCADE,
        related_name="Review"
    )

    rate_choices = [
        ("PS", "Позитивно"),
        ("NT", "Нейтрально"),
        ("NG", "Негативно")
    ]

    rate = models.CharField(
        verbose_name="Оценка",
        choices=rate_choices,
        max_length=2,
        default="NT"
    )

    class Meta:
        verbose_name = "Отзыва"
        verbose_name_plural = "Отзывы"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.user}-{self.meal}-{self.rate}"
