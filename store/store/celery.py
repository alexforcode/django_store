import os
import django
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

app = Celery('store')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
