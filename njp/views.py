import sys
from .models import *
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import PicForm
from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile


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
        context['title'] = "NJP"
        selected_tags = self.request.GET.getlist('tags')
        if selected_tags:
            selected_tags = selected_tags[0].split()
            filtered_pics = Pic.objects

            for tag in selected_tags:
                filtered_pics = filtered_pics.filter(tags__name=tag)

            context['pics_list'] = filtered_pics.distinct()

        return context


class AllTags(ListView):
    model = Tag
    template_name = 'njp/tags.html'
    context_object_name = 'tags'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Tags"
        return context

    def get_queryset(self):
        return Tag.objects.annotate(pic_count=Count('tags', distinct=True)).order_by('-pic_count')


class ShowPick(DetailView):
    model = Pic
    template_name = 'njp/show_pic.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'pic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['pic']
        return context


def upload_pic(request):
    if request.method == 'POST':
        form = PicForm(request.POST, request.FILES)
        tags_list = [tag.strip().lower() for tag in request.POST['tags'].split(',')]
        unique_tags = list(set(tags_list))
        unique_tags = [tag for tag in unique_tags if tag]
        exist_tags = [tag.name for tag in Tag.objects.all()]
        if form.is_valid():
            pic = form.save(commit=False)
            output_thumb = BytesIO()
            img = Image.open(pic.photo)
            img_name = pic.photo.name.split('.')[0]
            if img.height > 500 or img.width > 500:
                img.thumbnail((600, 350))
                img.save(output_thumb,format=img.format,quality=90)
            pic.photo_thumb_nail = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.{img.format}",
                                                       'image/jpeg', sys.getsizeof(output_thumb), None)
            pic.save()
            for i in unique_tags:
                if i in exist_tags:
                    a = Tag.objects.get(name=i)
                else:
                    a = Tag(name=i, slug=i)
                    a.save()
                pic.tags.add(a.id)

            return redirect('pic',
                            pk=pic.pk)
    else:
        form = PicForm()
    return render(request, 'njp/add_pic.html', {'form': form})
