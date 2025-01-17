from django.db import models
from users.models import User


class Ad(models.Model):
    """
    Модель для объявлений.
    """

    title = models.CharField(
        max_length=255,
        verbose_name="Название товара",
        help_text="Введите название товара",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена товара", help_text="Введите цену товара"
    )
    description = models.TextField(
        verbose_name="Описание товара", help_text="Добавьте описание товара"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="Автор объявления",
        help_text="Пользователь, который создал объявление",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания",
        help_text="Автоматически устанавливается при создании",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время обновления",
        help_text="Автоматически обновляется при редактировании",
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]  # Сортировка по дате создания (новые выше)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель для комментариев.
    """

    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор отзыва",
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Объявление",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время обновления",
        help_text="Автоматически обновляется при редактировании",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.email} - {self.ad.title}"
