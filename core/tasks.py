from celery import shared_task


@shared_task
def say_bye():
    return "bye bye"
