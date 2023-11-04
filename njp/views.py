from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.db.models import Count
from .models import *


class Index(ListView):
    model = Pic
    template_name = 'njp/index.html'
    context_object_name = 'pics_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_tags = Tag.objects.annotate(pic_count=Count('tags', distinct=True)).order_by('-pic_count')
        context['popular_tags'] = popular_tags
        context['tags'] = Tag.objects.all()
        return context
