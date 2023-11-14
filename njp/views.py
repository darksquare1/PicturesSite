import sys

from django.http import HttpResponseRedirect

from .models import *
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import PicForm
from io import BytesIO
from PIL import Image, ImageOps
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        is_liked = False
        ip = get_client_ip(request)
        if not IpModel.objects.filter(ip=ip).exists():
            IpModel.objects.create(ip=ip)
        if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
            is_liked = True
        else:
            is_liked = False
        context['is_liked'] = is_liked
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['pic']
        return context


def upload_pic(request):
    if request.method == 'POST':
        form = PicForm(request.POST, request.FILES)
        tags_list = [tag.strip().lower().replace(' ', '_') for tag in request.POST['tags'].split(',')]
        unique_tags = list(set(tags_list))
        unique_tags = [tag for tag in unique_tags if tag]
        exist_tags = [tag.name for tag in Tag.objects.all()]
        if form.is_valid():
            pic = form.save(commit=False)
            orig_pic_buffer = BytesIO()
            img = Image.open(pic.photo)
            img_name = pic.photo.name.split('.')[0]
            img = img.convert('RGB')
            orig_img = ImageOps.exif_transpose(img)
            orig_img.save(orig_pic_buffer, format='webp')
            pic.photo = InMemoryUploadedFile(orig_pic_buffer, 'ImageField', f"{img_name}.webp", f"image/webp",
                                             sys.getsizeof(orig_pic_buffer), None)
            if orig_img.height > 600 or orig_img.width > 600:
                output_thumb = BytesIO()
                orig_img.thumbnail((600, 600))
                fixed_image = orig_img.convert('RGB')
                fixed_image = ImageOps.exif_transpose(fixed_image)
                fixed_image.save(output_thumb, format='webp', quality=90)
                pic.photo_thumb_nail = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.webp",
                                                            f"image/webp", sys.getsizeof(output_thumb), None)
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
    return render(request, 'njp/add_pic.html', {'form': form, 'title': 'Upload'})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def picLike(request, pk):
    pic_id = request.POST.get('pic-id')
    pic = Pic.objects.get(pk=pic_id)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if pic.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        pic.likes.remove(IpModel.objects.get(ip=ip))
    else:
        pic.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('pic', args=[pic_id]))
