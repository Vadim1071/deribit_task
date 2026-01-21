"""
Celery задачи для получения и сохранения цен
"""
import time
import logging
import asyncio
from typing import Optional

from sqlalchemy.orm import Session

from deribit_task.celery_app import celery_app
from deribit_task.deribit_client import DeribitClient
from deribit_task.database import SessionLocal
from deribit_task.models import PriceTick

logger = logging.getLogger(__name__)


def save_price_tick(db: Session, ticker: str, price: float, timestamp: int) -> bool:
    """
    Сохраняет тик цены в базу данных
    
    :param db: Сессия БД
    :param ticker: Тикер валюты (BTC_USD или ETH_USD)
    :param price: Цена
    :param timestamp: Время в UNIX timestamp
    :return: True если успешно сохранено, False в противном случае
    """
    try:
        price_tick = PriceTick(
            ticker=ticker,
            price=price,
            timestamp=timestamp
        )
        db.add(price_tick)
        db.commit()
        logger.info(f"Сохранен тик: {ticker} = {price} в {timestamp}")
        return True
    except Exception as e:
        logger.error(f"Ошибка сохранения тика {ticker}: {e}")
        db.rollback()
        return False


async def fetch_and_save_prices(db: Session, timestamp: int):
    """
    Асинхронная функция для получения цен и сохранения в БД
    
    :param db: Сессия БД
    :param timestamp: Время в UNIX timestamp
    """
    async with DeribitClient() as client:
        # Получаем цену BTC
        btc_data = await client.get_btc_price()
        if btc_data and 'index_price' in btc_data:
            save_price_tick(db, 'BTC_USD', float(btc_data['index_price']), timestamp)
        else:
            logger.warning("Не удалось получить цену BTC")
        
        # Получаем цену ETH
        eth_data = await client.get_eth_price()
        if eth_data and 'index_price' in eth_data:
            save_price_tick(db, 'ETH_USD', float(eth_data['index_price']), timestamp)
        else:
            logger.warning("Не удалось получить цену ETH")


@celery_app.task(name='deribit_task.tasks.fetch_prices')
def fetch_prices():
    """
    Celery задача для получения цен BTC и ETH с биржи Deribit
    и сохранения их в базу данных
    """
    db: Optional[Session] = None
    try:
        db = SessionLocal()
        timestamp = int(time.time())
        
        # Запускаем асинхронную функцию
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        loop.run_until_complete(fetch_and_save_prices(db, timestamp))
        
    except Exception as e:
        logger.error(f"Ошибка в задаче fetch_prices: {e}")
    finally:
        if db:
            db.close()
