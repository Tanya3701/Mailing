from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(
        upload_to="users/avatars/", null=True, blank=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Телефон"
    )
    country = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Страна"
    )
    token = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="token"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("view_users", "view users"), ("block_users", "block users")]

    def __str__(self):
        return self.email
