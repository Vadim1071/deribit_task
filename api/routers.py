"""
Роутеры для API endpoints
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from deribit_task.database import get_db
from deribit_task.crud import PriceRepository
from deribit_task.api.schemas import PriceTickResponse, PriceTickListResponse, ErrorResponse
from deribit_task.config import SUPPORTED_TICKERS

router = APIRouter(prefix="/api/v1/prices", tags=["Prices"])


def validate_ticker(ticker: str) -> str:
    """
    Валидирует тикер валюты
    
    :param ticker: Тикер для валидации
    :return: Валидный тикер
    :raises HTTPException: Если тикер не поддерживается
    """
    if ticker not in SUPPORTED_TICKERS:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый тикер. Поддерживаемые тикеры: {', '.join(SUPPORTED_TICKERS)}"
        )
    return ticker


@router.get("/all", response_model=PriceTickListResponse)
def get_all_prices(
    ticker: str = Query(..., description="Тикер валюты (BTC_USD или ETH_USD)"),
    db: Session = Depends(get_db)
):
    """
    Получение всех сохраненных данных по указанной валюте
    
    - **ticker**: Тикер валюты (обязательный параметр)
    """
    validate_ticker(ticker)
    
    price_ticks = PriceRepository.get_all_by_ticker(db, ticker)
    
    return PriceTickListResponse(
        ticker=ticker,
        count=len(price_ticks),
        data=[PriceTickResponse.model_validate(tick) for tick in price_ticks]
    )


@router.get("/latest", response_model=PriceTickResponse)
def get_latest_price(
    ticker: str = Query(..., description="Тикер валюты (BTC_USD или ETH_USD)"),
    db: Session = Depends(get_db)
):
    """
    Получение последней цены валюты
    
    - **ticker**: Тикер валюты (обязательный параметр)
    """
    validate_ticker(ticker)
    
    latest_tick = PriceRepository.get_latest_price(db, ticker)
    
    if not latest_tick:
        raise HTTPException(
            status_code=404,
            detail=f"Цены для тикера {ticker} не найдены"
        )
    
    return PriceTickResponse.model_validate(latest_tick)


@router.get("/filter", response_model=PriceTickListResponse)
def get_price_by_date(
    ticker: str = Query(..., description="Тикер валюты (BTC_USD или ETH_USD)"),
    date_from: Optional[int] = Query(None, description="Начальная дата в UNIX timestamp"),
    date_to: Optional[int] = Query(None, description="Конечная дата в UNIX timestamp"),
    db: Session = Depends(get_db)
):
    """
    Получение цены валюты с фильтром по дате
    
    - **ticker**: Тикер валюты (обязательный параметр)
    - **date_from**: Начальная дата в UNIX timestamp (опционально)
    - **date_to**: Конечная дата в UNIX timestamp (опционально)
    """
    validate_ticker(ticker)
    
    price_ticks = PriceRepository.get_price_by_date(db, ticker, date_from, date_to)
    
    return PriceTickListResponse(
        ticker=ticker,
        count=len(price_ticks),
        data=[PriceTickResponse.model_validate(tick) for tick in price_ticks]
    )
