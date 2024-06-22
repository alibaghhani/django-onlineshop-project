import os
from datetime import timedelta

from celery import Celery
from django.apps import apps

from config import settings

# from config.settings import CELERY_BROKER_URL

# ---- celery configuration -----
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
