from django import forms
from .models import Post, Category

class NewsSearchForm(forms.Form):
    post_title = forms.CharField(label='Название новости', required=False)
    category_names = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', required=False)
