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
        all_tags = Tag.objects.all()
        popular_tags = all_tags.annotate(pic_count=Count('tags', distinct=True)).order_by('-pic_count')
        context['popular_tags'] = popular_tags
        context['all_tags'] = Tag.objects.all()
        context['title'] = "NJP Home"
        return context


class AllTags(ListView):
    model = Tag
    template_name = 'njp/tags.html'
    context_object_name = 'tags'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = "Tags"
        return context

    def get_queryset(self):
        return Tag.objects.annotate(pic_count=Count('tags', distinct=True)).order_by('-pic_count')
