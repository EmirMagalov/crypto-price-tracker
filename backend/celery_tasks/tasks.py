import aiohttp
import time
import redis
import json
from celery import shared_task
from database.connection import session_local
from models.price import Price
from asgiref.sync import async_to_sync
from core.config import settings

base_redis = settings.base_redis
deribit_url = settings.deribit_url
r = redis.Redis(host=base_redis, port=6379, db=0)


async def get_prices():
    async with aiohttp.ClientSession() as session:
        db = session_local()
        try:
            for ticker in ["btc_usd", "eth_usd"]:
                url = deribit_url.format(currency=ticker)
                async with session.get(url) as resp:
                    data = await resp.json()
                    price_value = data["result"]["index_price"]
                    price = Price(
                        ticker=ticker, price=price_value, timestamp=int(time.time())
                    )
                    db.add(price)
                    db.commit()
                    db.refresh(price)
                    msg = {
                        "ticker": price.ticker,
                        "price": price.price,
                        "timestamp": price.timestamp,
                    }
                    r.publish("prices_channel", json.dumps(msg))
        finally:
            db.close()


@shared_task
def prices_task():
    async_to_sync(get_prices)()
