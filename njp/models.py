from django.db import models


class Pic(models.Model):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    tags = models.ManyToManyField('Tag', blank=False, related_name='tags', verbose_name='Теги')

    def get_likes_count(self):
        return self.likes.count()

    class Meta:
        verbose_name = "Картинки"
        verbose_name_plural = 'Картинки'
        ordering = ['-time_create']

    def __str__(self):
        return f"Картинка {self.id}"


class Like(models.Model):
    pic = models.ForeignKey(Pic, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ('pic', 'ip_address')


class Tag(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя тега')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name