# Kлиент для криптобиржи Deribit

## Crypto Price Tracker

Сервис для сбора, хранения и отображения текущих цен криптовалют BTC и ETH с биржи Deribit с визуализацией последних цен в реальном времени.

![Main menu](images/main1.png)

![Main menu](images/main2.png)

### Используемые технологии

* Python 3.11 – бэкенд
* FastAPI – REST API + WebSocket
* PostgreSQL – база данных для хранения исторических цен
* SQLAlchemy – ORM
* Celery + Redis – периодический сбор цен
* aiohttp – асинхронный клиент для Deribit
* Vue 3 + Vite – фронтенд для отображения последних цен
* Redis pub/sub – передача новых цен с бэкенда на фронтенд через WebSocket
* Docker + Docker Compose – контейнеризация приложения
* Pytest – unit тесты
