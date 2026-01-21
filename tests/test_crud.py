"""
Unit тесты для CRUD операций
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

from deribit_task.database import Base
from deribit_task.models import PriceTick
from deribit_task.crud import PriceRepository


@pytest.fixture
def db_session():
    """Фикстура для создания тестовой БД"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Добавляем тестовые данные
    tick1 = PriceTick(ticker='BTC_USD', price=Decimal('50000.5'), timestamp=1000000)
    tick2 = PriceTick(ticker='BTC_USD', price=Decimal('51000.0'), timestamp=1000060)
    tick3 = PriceTick(ticker='ETH_USD', price=Decimal('3000.25'), timestamp=1000000)
    
    session.add(tick1)
    session.add(tick2)
    session.add(tick3)
    session.commit()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


def test_get_all_by_ticker(db_session):
    """Тест получения всех тиков по тикеру"""
    ticks = PriceRepository.get_all_by_ticker(db_session, 'BTC_USD')
    
    assert len(ticks) == 2
    assert ticks[0].ticker == 'BTC_USD'
    assert ticks[0].price == Decimal('50000.5')


def test_get_latest_price(db_session):
    """Тест получения последней цены"""
    latest = PriceRepository.get_latest_price(db_session, 'BTC_USD')
    
    assert latest is not None
    assert latest.ticker == 'BTC_USD'
    assert latest.price == Decimal('51000.0')
    assert latest.timestamp == 1000060


def test_get_price_by_date(db_session):
    """Тест получения цен с фильтром по дате"""
    ticks = PriceRepository.get_price_by_date(
        db_session, 
        'BTC_USD', 
        date_from=1000000,
        date_to=1000030
    )
    
    assert len(ticks) == 1
    assert ticks[0].timestamp == 1000000


def test_get_price_by_date_no_results(db_session):
    """Тест получения цен с фильтром по дате без результатов"""
    ticks = PriceRepository.get_price_by_date(
        db_session,
        'BTC_USD',
        date_from=2000000
    )
    
    assert len(ticks) == 0
