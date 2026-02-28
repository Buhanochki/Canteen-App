from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.ingredients.models import Ingredient
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.apps.users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, TimedBaseModel):
    username = None

    first_name = models.CharField(
        verbose_name="first name",
        max_length=150,
    )

    last_name = models.CharField(
        verbose_name="last name",
        max_length=150,
    )

    surname = models.CharField(
        verbose_name="surname",
        max_length=150,
        blank=True,
    )

    email = models.EmailField(
        verbose_name="email",
        unique=True,
        error_messages={"unique": "Пользователь с такой почтой уже зарегистрировался"},
    )

    STATUS_CHOICES = [
        ("PT", "Ученик"),
        ("TC", "Повар"),
        ("AD", "Админ"),
    ]

    status = models.CharField(
        verbose_name="user status",
        max_length=2,
        choices=STATUS_CHOICES,
        default="PT",
    )

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
    )

    is_active = models.BooleanField(
        ("active"),
        default=True,
    )

    allergies = models.ManyToManyField(
        Ingredient,
        verbose_name="Аллергии",
        blank=True
    )

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["pk"]
        db_table = "custom_users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
