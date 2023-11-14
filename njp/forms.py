from django import forms
from .models import Pic


class PicForm(forms.ModelForm):
    class Meta:
        model = Pic
        fields = ['photo', 'tags']

    tags = forms.CharField(max_length=255, required=True, label='Теги', help_text='Введите теги через запятую')
