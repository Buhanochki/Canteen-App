from django.db import models
from core.apps.common.models import TimedBaseModel
from core.apps.items.models import Item
from core.apps.users.models import CustomUser

class Meal(TimedBaseModel):
    day = models.ForeignKey(
        'Day',
        verbose_name="День проведения",
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField(
        Item,
        verbose_name="Блюда",
        related_name="meals"
    )
    user = models.ManyToManyField(
        CustomUser,
        through='UserMeal'
    )
    cost = models.IntegerField(
        verbose_name="Цена",
    )

    categories = [
        ('BF', 'Завтрак'),
        ('DN', 'Обед')
    ]

    category = models.CharField(
        choices=categories,
        max_length=2,
        default='BF'
    )

    is_prepared = models.BooleanField(
        verbose_name="Приготовлен ли",
        default=False,
    )

    class Meta:
        verbose_name = "Прием пищи"
        verbose_name_plural = "Приемы пищи"
        ordering = ["pk"]
        unique_together = ['day', 'category']

    def __str__(self):
        return f"{self.day}-{self.category}"
    

class UserMeal(TimedBaseModel):
    user = models.ForeignKey(
        CustomUser,
        verbose_name="пользователь",
        on_delete=models.CASCADE
    )
    meal = models.ForeignKey(
        Meal,
        verbose_name="Прием пищи",
        on_delete=models.CASCADE
    )
    is_given = models.BooleanField(
        default=0,
        verbose_name="Выдан",
    )

    class Meta:
        unique_together = ['user', 'meal']
        verbose_name = "Пользователь-Прием Пищи"
        verbose_name_plural = "Записи"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.user}-{self.meal}"
    

class Day(TimedBaseModel):
    date = models.DateField(
        verbose_name="Дата",
        unique=True,
    )

    class Meta:
        verbose_name = "День"
        verbose_name_plural = "Дни"
        ordering = ['pk']
    

    def __str__(self):
        return f"{self.date}"
