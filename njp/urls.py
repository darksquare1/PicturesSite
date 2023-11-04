from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('tags/', AllTags.as_view(), name='tags'),
]
