from django.contrib import admin
from .models import *


class PicAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'time_create', 'get_tags')
    filter_horizontal = ('tags',)  # Добавляем эту строку для удобства выбора тегов

    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Теги'

admin.site.register(Pic, PicAdmin)
admin.site.register(Like)
admin.site.register(Tag)
