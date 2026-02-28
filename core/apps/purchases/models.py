from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.ingredients.models import Ingredient
from core.apps.users.models import CustomUser


class Purchase(TimedBaseModel):
    title = models.CharField(max_length=20, verbose_name="Название")
    
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        related_name="purchases",
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Создатель закупки",
        on_delete=models.CASCADE,
    )
    is_approved = models.BooleanField(
        verbose_name="Принята",
        default=False,
    )

    amount = models.IntegerField(
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = "Закупка"
        verbose_name_plural = "Закупки"
        ordering = ['pk']

    def __str__(self):
        return f"{self.author}-{self.title}"
    