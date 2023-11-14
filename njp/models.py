from django.db import models
from django.urls import reverse


class IpModel(models.Model):
    ip = models.CharField(max_length=128)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Айпишник"
        verbose_name_plural = 'Айпишник'


class Pic(models.Model):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', verbose_name='Фото')
    photo_thumb_nail = models.ImageField(upload_to='users/thumbs/%Y/%m/%d/', blank=True, verbose_name='thumbnail')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    tags = models.ManyToManyField('Tag', blank=False, related_name='tags', verbose_name='Теги')
    likes = models.ManyToManyField(IpModel, related_name='pic_likes', blank=True)

    def get_likes_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('pic', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Картинки"
        verbose_name_plural = 'Картинки'
        ordering = ['-time_create']

    def __str__(self):
        return f"Изображение №{self.pk}"


class Tag(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя тега')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
