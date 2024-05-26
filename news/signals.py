# signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.models import Site
from .models import Post, Subscriber

@receiver(m2m_changed, sender=Post.category_names.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.category_names.all()
        subscribers = Subscriber.objects.filter(category__in=categories).select_related('user')
        
        post_url = reverse('post_detail', kwargs={'pk': instance.pk})
        full_url = f'http://127.0.0.1:8000{post_url}'

        for subscriber in subscribers:
            send_mail(
                subject=f'Новый пост',
                message=f'Читать полностью: {instance.post_title}\n{full_url}',
                from_email='no-reply@example.com',
                recipient_list=[subscriber.user.email],
            )
