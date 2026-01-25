import os
import aiohttp
import asyncio
import time
import redis
import json
from celery import shared_task
from database import session_local
from models import Price
from dotenv import load_dotenv
from asgiref.sync import async_to_sync
load_dotenv()
redis_url = os.getenv("REDIS_URL")
DERIBIT_URL = "https://test.deribit.com/api/v2/public/get_index_price?index_name={currency}"
redis_url = redis_url.replace('redis://', '')
r = redis.Redis(host=redis_url, port=6379, db=0)


async def get_prices():
    async with aiohttp.ClientSession() as session:
        db = session_local()
        try:
            for ticker in ["btc_usd", "eth_usd"]:
                url = DERIBIT_URL.format(currency=ticker)
                async with session.get(url) as resp:
                    data = await resp.json()
                    price_value = data["result"]["index_price"]
                    price = Price(
                        ticker=ticker,
                        price=price_value,
                        timestamp=int(time.time())
                    )
                    db.add(price)
                    db.commit()
                    db.refresh(price)
                    msg = {
                        "ticker": price.ticker,
                        "price": price.price,
                        "timestamp": price.timestamp
                    }
                    r.publish("prices_channel", json.dumps(msg))
        finally:
            db.close()


@shared_task
def prices_task():
    async_to_sync(get_prices)()
