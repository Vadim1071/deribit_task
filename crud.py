"""
CRUD операции для работы с ценами
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from deribit_task.models import PriceTick


class PriceRepository:
    """
    Репозиторий для работы с ценами криптовалют
    """

    @staticmethod
    def get_all_by_ticker(db: Session, ticker: str) -> List[PriceTick]:
        """
        Получает все сохраненные данные по указанной валюте
        
        :param db: Сессия БД
        :param ticker: Тикер валюты (BTC_USD или ETH_USD)
        :return: Список всех тиков для указанного тикера
        """
        return db.query(PriceTick).filter(PriceTick.ticker == ticker).order_by(PriceTick.timestamp).all()

    @staticmethod
    def get_latest_price(db: Session, ticker: str) -> Optional[PriceTick]:
        """
        Получает последнюю цену валюты
        
        :param db: Сессия БД
        :param ticker: Тикер валюты (BTC_USD или ETH_USD)
        :return: Последний тик цены или None
        """
        return db.query(PriceTick).filter(PriceTick.ticker == ticker).order_by(desc(PriceTick.timestamp)).first()

    @staticmethod
    def get_price_by_date(db: Session, ticker: str, date_from: Optional[int] = None, date_to: Optional[int] = None) -> List[PriceTick]:
        """
        Получает цены валюты с фильтром по дате
        
        :param db: Сессия БД
        :param ticker: Тикер валюты (BTC_USD или ETH_USD)
        :param date_from: Начальная дата в UNIX timestamp (опционально)
        :param date_to: Конечная дата в UNIX timestamp (опционально)
        :return: Список тиков, отфильтрованных по дате
        """
        query = db.query(PriceTick).filter(PriceTick.ticker == ticker)
        
        if date_from:
            query = query.filter(PriceTick.timestamp >= date_from)
        
        if date_to:
            query = query.filter(PriceTick.timestamp <= date_to)
        
        return query.order_by(PriceTick.timestamp).all()
