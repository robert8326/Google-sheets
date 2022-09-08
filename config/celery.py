from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('google_sheets')

app.conf.beat_schedule = {
    'update_data': {  # Для обновления данных
        'task': 'google_sheets.update_data',
        'schedule': crontab(minute='*/1'),  # Время работы таска
    },
}

app.autodiscover_tasks()
app.config_from_object('django.conf:settings', namespace='CELERY')
