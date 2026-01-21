"""
Unit тесты для API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

from deribit_task.main import app
from deribit_task.database import Base, get_db
from deribit_task.models import PriceTick


@pytest.fixture
def test_db():
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
    
    def override_get_db():
        try:
            yield session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """Фикстура для тестового клиента"""
    return TestClient(app)


def test_get_all_prices(client):
    """Тест получения всех цен"""
    response = client.get("/api/v1/prices/all?ticker=BTC_USD")
    
    assert response.status_code == 200
    data = response.json()
    assert data['ticker'] == 'BTC_USD'
    assert data['count'] == 2
    assert len(data['data']) == 2


def test_get_all_prices_invalid_ticker(client):
    """Тест получения всех цен с невалидным тикером"""
    response = client.get("/api/v1/prices/all?ticker=INVALID")
    
    assert response.status_code == 400


def test_get_latest_price(client):
    """Тест получения последней цены"""
    response = client.get("/api/v1/prices/latest?ticker=BTC_USD")
    
    assert response.status_code == 200
    data = response.json()
    assert data['ticker'] == 'BTC_USD'
    assert data['price'] == 51000.0


def test_get_latest_price_not_found(client):
    """Тест получения последней цены для несуществующего тикера"""
    response = client.get("/api/v1/prices/latest?ticker=UNKNOWN_USD")
    
    assert response.status_code == 404


def test_get_price_by_date(client):
    """Тест получения цен с фильтром по дате"""
    response = client.get("/api/v1/prices/filter?ticker=BTC_USD&date_from=1000000&date_to=1000030")
    
    assert response.status_code == 200
    data = response.json()
    assert data['ticker'] == 'BTC_USD'
    assert len(data['data']) == 1


def test_get_price_by_date_no_ticker(client):
    """Тест получения цен без указания тикера"""
    response = client.get("/api/v1/prices/filter")
    
    assert response.status_code == 422  # Validation error
