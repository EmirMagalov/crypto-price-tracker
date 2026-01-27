from celery import shared_task
from asgiref.sync import async_to_sync
from celery_tasks.price_func import get_prices


@shared_task
def prices_task():
    async_to_sync(get_prices)()
