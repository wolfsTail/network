from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model
    """
    friends = models.ManyToManyField("self", blank=True, symmetrical=True, verbose_name="Друзья")

    class Meta:
        db_table = "users"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
