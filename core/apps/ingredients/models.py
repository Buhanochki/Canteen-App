from django.db import models
from core.apps.common.models import TimedBaseModel

class Ingredient(TimedBaseModel):
    title = models.CharField(
        verbose_name="Название",
        max_length=20
    )

    amount = models.IntegerField(
        verbose_name="Количество",
        default=0
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.title}"

