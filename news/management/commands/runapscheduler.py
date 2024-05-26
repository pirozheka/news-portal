import logging

from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.utils.timezone import now
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from news.models import Post, Subscriber, Category
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    one_week_ago = now() - timedelta(days=7)
    
    # Получаем всех подписчиков
    subscribers = Subscriber.objects.all()
    
    for subscriber in subscribers:
        # Получаем пользователя и категории, на которые он подписан
        user = subscriber.user
        
        # Получаем все посты, опубликованные за последнюю неделю и относящиеся к категориям подписчика
        posts = Post.objects.filter(post_created__gte=one_week_ago)

        # Формируем сообщение для отправки
        message = f"Привет, {user.username}!\n\nНовые посты за неделю:\n\n"
        for post in posts:
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
       
    


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(day_of_week='sun', minute="34", hour="20"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")