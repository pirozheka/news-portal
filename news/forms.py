from django import forms
from .models import Post, Category, Subscriber

class NewsSearchForm(forms.Form):
    post_title = forms.CharField(label='Название новости', required=False)
    category_names = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', required=False)

class SubscriptionForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)