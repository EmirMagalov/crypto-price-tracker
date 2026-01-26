import asyncio
import os
from fastapi import FastAPI
from models.price import Base
from database.connection import engine
from fastapi.middleware.cors import CORSMiddleware
from core.redis_manager import redis_listener
from routers import views
from core.config import settings
async def lifespan(app: FastAPI):
    # Startup
    app.state.redis_task = asyncio.create_task(redis_listener())
    print("Redis listener started")
    yield
    # Shutdown
    app.state.redis_task.cancel()
    try:
        await app.state.redis_task
    except asyncio.CancelledError:
        print("Redis listener cancelled")


app = FastAPI(lifespan=lifespan)
app.include_router(views.router)
# origins = os.getenv("FRONTEND_ORIGINS", "").split(",")
origins = settings.frontend_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)





