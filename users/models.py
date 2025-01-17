from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
    ]
    username = None
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона"
    )
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="user")
    avatar = models.ImageField(
        upload_to="users/avatars/", **NULLABLE, help_text="Загрузите свой аватар"
    )
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
