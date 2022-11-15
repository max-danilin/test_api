import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_api.settings')

app = Celery('test_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


