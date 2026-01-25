import os
import json
import asyncio
import redis.asyncio as aioredis
from ws_manager import ConnectionManager
from dotenv import load_dotenv
load_dotenv()
manager = ConnectionManager()

redis_url = os.getenv("REDIS_URL")

async def redis_listener():
    redis = aioredis.from_url(f"{redis_url}:6379/0")
    pubsub = redis.pubsub()
    await pubsub.subscribe("prices_channel")
    print("Subscribed to Redis channel")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message is not None:
                data = json.loads(message['data'])
                print("Redis message received:", data)
                await manager.send_message(data)
            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        print("Redis listener stopping...")
        await pubsub.close()
        await redis.close()
