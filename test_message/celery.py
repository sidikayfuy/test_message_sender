import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_message.settings')


app = Celery('test_message')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()