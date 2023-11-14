from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('tags/', AllTags.as_view(), name='tags'),
    path('pic/<int:pk>/', ShowPick.as_view(), name="pic"),
    path('upload/', upload_pic, name='upload'),
    path('like/<int:pk>', picLike, name='pic_like'),
]
