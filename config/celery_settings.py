from celery import Celery
from datetime import timedelta
import os
# ---- celery configuration -----
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.autodiscover_tasks()
app.conf.broker_url = "redis://127.0.0.1:6379/0"
app.conf.result_backend = "redis://10.10.10.10:6379/0"
app.conf.accept_content = ["json"]
app.conf.result_expires = timedelta(days=1)
app.conf.task_always_eager = False
app.conf.worker_prefetch_multiplier = 1
