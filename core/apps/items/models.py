from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.users.models import CustomUser
from core.apps.ingredients.models import Ingredient

class Item(TimedBaseModel):
    title = models.CharField(
        max_length=20,
        verbose_name="Название",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        through='IngredientItem',
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.title}"
    
class IngredientItem(TimedBaseModel):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиент",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        verbose_name="Блюдо",
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name="Количество",
        default=1
    )
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Ингридиент-Продукт"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.ingredient}-{self.item}-{self.amount}"
