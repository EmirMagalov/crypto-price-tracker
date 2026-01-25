import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()
redis_url = os.getenv("REDIS_URL")
celery_app = Celery(
    "worker",
    broker=f"{redis_url}:6379/0",
    backend=f"{redis_url}:6379/1"
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "tasks.prices_task",
        "schedule": 60.0,
    }
}

celery_app.conf.timezone = "UTC"

import tasks
