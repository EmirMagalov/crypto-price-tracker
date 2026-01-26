from models.price import Price
import time


def test_get_prices(client, db):
    price = Price(
        ticker="btc_usd",
        price=50000,
        timestamp=int(time.time())
    )
    db.add(price)
    db.commit()

    response = client.get("/prices/?ticker=btc_usd")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ticker"] == "btc_usd"


def test_get_latest_price(client, db):
    db.add_all([
        Price(ticker="btc_usd", price=100, timestamp=1),
        Price(ticker="btc_usd", price=200, timestamp=2),
    ])
    db.commit()

    response = client.get("/prices/latest/?ticker=btc_usd")

    assert response.status_code == 200
    assert response.json()["price"] == 200


def test_filter_by_time(client, db):
    db.add(
        Price(ticker="btc_usd", price=200, timestamp=1769179267),

    )
    db.commit()

    response = client.get(
        "/prices/filter/?ticker=btc_usd&date_ts=1769179267"
    )

    data = response.json()

    assert data["price"] == 200
    assert data["ticker"] == "btc_usd"
