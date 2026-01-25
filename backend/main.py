import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket
from models import Base, Price
from database import engine, session_local
from schemas import Price as Db_Price
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from redis_manager import redis_listener, manager


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

origins = os.getenv("FRONTEND_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/prices/limit/", response_model=List[Db_Price])
def get_prices(ticker: str = Query(..., description="Ticker валюты"), db: Session = Depends(get_db)):
    prices = (
        db.query(Price)
        .filter(Price.ticker == ticker.lower())
        .order_by(Price.timestamp.desc())
        .limit(5)
        .all()
    )
    if not prices:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return prices


@app.get("/prices/", response_model=List[Db_Price])
def get_prices(ticker: str = Query(..., description="Ticker валюты"), db: Session = Depends(get_db)):
    prices = db.query(Price).filter(Price.ticker == ticker.lower()).all()
    if not prices:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return prices


@app.get("/prices/latest/", response_model=Db_Price)
def get_latest_price(ticker: str = Query(..., description="Ticker валюты"), db: Session = Depends(get_db)):
    price = db.query(Price).filter(Price.ticker == ticker.lower()).order_by(Price.timestamp.desc()).first()

    if not price:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return price


@app.get("/prices/filter/", response_model=Db_Price)
def get_prices_by_date(
        ticker: str = Query(...),
        date_ts: int = Query(...),
        db: Session = Depends(get_db)
):
    day_start = datetime.fromtimestamp(date_ts).replace(hour=0, minute=0, second=0)
    day_end = day_start + timedelta(days=1)

    price = (
        db.query(Price)
        .filter(
            Price.ticker == ticker.lower(),
            Price.timestamp >= int(day_start.timestamp()),
            Price.timestamp < int(day_end.timestamp())
        )
        .order_by(Price.timestamp.desc())
        .first()
    )

    if not price:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return price


@app.websocket("/ws/prices/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)
