from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django import forms
from .models import Post, Category, Author, Subscriber
from .filters import NewsFilter
from .forms import NewsSearchForm, SubscriptionForm

from newspaper.tasks import send_notification




class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_created'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news-page.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts_list'
    paginate_by = 10

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context
    
class NewsSearch(ListView):
    model = Post
    ordering = '-post_created'
    template_name = 'news-search.html'
    context_object_name = 'posts_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    


class PostDetail(DetailView):
    model = Post
    template_name = 'post-detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context
    
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
        'author', 'post_title', 'post_text', 'category_names'
    ]


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostCreateForm
    model = Post
    template_name = 'post_create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NP'
        post.save()
        send_notification.apply_async([post.pk])
        return super().form_valid(form)
    
    
    
class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostCreateForm
    model = Post
    template_name = 'post_create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)

class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostCreateForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

@login_required
def subscriptions(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Удаляем существующие подписки пользователя
            Subscriber.objects.filter(user=request.user).delete()
            # Добавляем новые подписки
            for category in form.cleaned_data['categories']:
                Subscriber.objects.get_or_create(user=request.user, category=category)
            # Добавляем сообщение
            messages.success(request, 'Подписки обновлены')
            return redirect('subscriptions')
    else:
        # Получаем категории, на которые подписан пользователь
        subscribed_categories = Subscriber.objects.filter(user=request.user).values_list('category', flat=True)
        form = SubscriptionForm(initial={'categories': subscribed_categories})
    return render(request, 'subscriptions.html', {'form': form})