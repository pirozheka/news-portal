from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from news.models import Post
from datetime import datetime, timedelta
from django.utils.timezone import now

@shared_task
def send_notification(post_pk):
    post = Post.objects.get(id=post_pk)
    categories = set(post.category_names.values_list('category_name', flat=True))
    users = set(User.objects.filter(subscriber__category__category_name__in=categories))
   
    for user in users:  
        message = f"Привет, {user.username}!\n\nНовые посты за неделю:\n\n"
        message += f"{post.post_title}\n"
        message += f"URL: http://127.0.0.1{post.get_absolute_url()}\n\n"
        
        # Отправляем сообщение на почту пользователя
        send_mail(
            'Weekly Newsletter',
            message,
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

@shared_task
def send_weekly_newsletter():
    one_week_ago = now() - timedelta(days=7)

    # Получаем все посты, опубликованные за последнюю неделю
    posts = Post.objects.filter(post_created__gte=one_week_ago)

    # Получаем категории
    categories = set(post.category_names.values_list('category_name', flat=True) for post in posts)
    # Получаем список подписчиков
    users = set(User.objects.filter(subscriber__category__category_name__in=categories))

       
    for user in users:
        sub_cat = user.subscriber.values_list('category__category_name', flat=True)
        posts_cat_sub = posts.filter(category_names__category_name__in=sub_cat)
        
        # Формируем сообщение для отправки
        message = f"Привет, {user.username}!\n\nНовые посты за неделю:\n\n"
        for post in posts_cat_sub:
            message += f"{post.post_title}\n"
            message += f"URL: http://127.0.0.1{post.get_absolute_url()}\n\n"
        
        # Отправляем сообщение на почту пользователя
        send_mail(
            'Weekly Newsletter',
            message,
            'from@example.com',
            [user.email],
            fail_silently=False,
        )