import aiohttp
import time
import redis
import json

from database.connection import session_local
from models.price import Price

from core.config import settings
TICKERS = ("btc_usd", "eth_usd")
redis_host = settings.redis_host
deribit_url = settings.deribit_url + '/get_index_price?index_name={currency}'
r = redis.Redis(host=redis_host, port=6379, db=0)

async def fetch_index_price(session: aiohttp.ClientSession, url: str) -> float:
    async with session.get(url) as resp:
        resp.raise_for_status()
        payload = await resp.json()
    return payload["result"]["index_price"]


def save_and_publish(db, ticker: str, price_value: float) -> None:
    ts = int(time.time())

    price = Price(ticker=ticker, price=price_value, timestamp=ts)
    db.add(price)
    db.commit()
    db.refresh(price)

    msg = {"ticker": price.ticker, "price": price.price, "timestamp": price.timestamp}
    r.publish("prices_channel", json.dumps(msg))


async def process_ticker(session: aiohttp.ClientSession, db, ticker: str) -> None:
    url = deribit_url.format(currency=ticker)
    price_value = await fetch_index_price(session, url)
    save_and_publish(db, ticker, price_value)


async def get_prices() -> None:
    db = session_local()
    try:
        async with aiohttp.ClientSession() as session:
            for ticker in TICKERS:
                await process_ticker(session, db, ticker)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
