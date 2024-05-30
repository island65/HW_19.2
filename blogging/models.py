from django.db import models
from django.utils.text import slugify

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name="заголовок")
    slug = models.CharField(max_length=250, **NULLABLE, verbose_name="slug")
    body = models.TextField(verbose_name="содержимое")
    image = models.ImageField(upload_to="blog", verbose_name="изображение", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    is_published = models.BooleanField(default=True, verbose_name="признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="количество просмотров")


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
