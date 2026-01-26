import os
from celery import Celery
from core.config import settings
redis_url = settings.redis_url
celery_app = Celery(
    "worker",
    broker=f"{redis_url}:6379/0",
    backend=f"{redis_url}:6379/1"
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "celery_tasks.tasks.prices_task",
        "schedule": 60.0,
    }
}

celery_app.conf.timezone = "UTC"

import celery_tasks.tasks
