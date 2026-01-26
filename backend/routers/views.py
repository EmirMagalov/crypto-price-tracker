from fastapi import APIRouter,HTTPException, Query, Depends
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket
from models.price import Price
from schemas.schemas import Price as Db_Price
from core.redis_manager import manager
from database.dependencies import get_db


router = APIRouter()


@router.get("/prices/limit/", response_model=List[Db_Price])
def get_limit_prices(ticker: str = Query(..., description="Ticker валюты"), db: Session = Depends(get_db)):
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


@router.get("/prices/", response_model=List[Db_Price])
def get_prices(ticker: str = Query(..., description="Ticker валюты"), db: Session = Depends(get_db)):
    prices = db.query(Price).filter(Price.ticker == ticker.lower()).all()
    if not prices:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return prices


@router.get("/prices/latest/", response_model=Db_Price)
def get_latest_price(ticker: str = Query(..., description="Ticker валюты"), db: Session = Depends(get_db)):
    price = db.query(Price).filter(Price.ticker == ticker.lower()).order_by(Price.timestamp.desc()).first()

    if not price:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return price


@router.get("/prices/filter/", response_model=Db_Price)
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


@router.websocket("/ws/prices/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)