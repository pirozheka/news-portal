import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')
 
app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_newsletter_every_monday_8am': {
        'task': 'send_weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}