from pydantic import BaseModel


class PriceBase(BaseModel):
    ticker: str
    price: float
    timestamp: int


class PriceCreate(PriceBase): ...


class Price(PriceBase):
    id: int

    class Config:
        orm_mode = True
