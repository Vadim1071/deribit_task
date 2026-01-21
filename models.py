"""
Модели базы данных для хранения цен криптовалют
"""
from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Index
from sqlalchemy.sql import func

from deribit_task.database import Base


class PriceTick(Base):
    """
    Модель для хранения тиков цен криптовалют
    """
    __tablename__ = 'price_ticks'

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    price = Column(Numeric(precision=20, scale=8), nullable=False)
    timestamp = Column(BigInteger, nullable=False, index=True)

    # Индекс для быстрого поиска по тикеру и времени
    __table_args__ = (
        Index('idx_ticker_timestamp', 'ticker', 'timestamp'),
    )

    def __repr__(self):
        return f"<PriceTick(ticker={self.ticker}, price={self.price}, timestamp={self.timestamp})>"
