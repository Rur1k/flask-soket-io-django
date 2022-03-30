from celery import shared_task
from .models import User


@shared_task(bind=True, track_started=True)
def update_mongobd():
    pass