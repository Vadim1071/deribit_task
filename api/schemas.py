"""
Pydantic схемы для валидации данных API
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class PriceTickResponse(BaseModel):
    """
    Схема ответа для тика цены
    """
    id: int
    ticker: str
    price: Decimal
    timestamp: int

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: str
        }


class PriceTickListResponse(BaseModel):
    """
    Схема ответа для списка тиков
    """
    ticker: str
    count: int
    data: List[PriceTickResponse]


class ErrorResponse(BaseModel):
    """
    Схема ответа для ошибок
    """
    error: str
    detail: Optional[str] = None
