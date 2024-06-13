from celery import Celery
from config.settings import CELERY_BROKER_URL
from account.models import Address

app = Celery('tasks',broker=CELERY_BROKER_URL)

@app.task
def add():
    address_to_delete = Address.objects.get(costumer=1)
    address_to_delete.delete()

    return 4
