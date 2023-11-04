from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import *


class Index(ListView):
    model = Pic
    template_name = 'njp/index.html'
    context_object_name = 'pics_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context
