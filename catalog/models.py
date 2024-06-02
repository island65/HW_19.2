from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    objects = None
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание", **NULLABLE, help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание", **NULLABLE, help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="catalog/photo",
        verbose_name="Фото",
        **NULLABLE,
        help_text="Загрузите фото продукта",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Введите цену продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        related_name="Наименование",
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата изменения"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создан пользователем",
        **NULLABLE,
    )

    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Счётчик просмотров",
        help_text="Укажите количество просмотров",
    )

    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        permissions = [
            ('set_published_status', 'Can publish product'),
            ('change_description', 'Can change product description'),
            ('change_category', 'Can change product category'),
        ]

    def __str__(self):
        return f"{self.name} {self.price}"


class Version(models.Model):
    product = models.ForeignKey(
        Products,
        related_name="version",
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Продукт",
    )
    version_number = models.PositiveIntegerField(
        verbose_name="Номер версии",
        help_text="Введите номер версии продукта",
    )
    version_title = models.CharField(
        max_length=150,
        verbose_name="Название версии",
        help_text="Введите название версии",
    )
    version_is_active = models.BooleanField(
        default=False, verbose_name="Признак текущей версии"
    )

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"

    def __str__(self):
        return f"{self.version_title}"
