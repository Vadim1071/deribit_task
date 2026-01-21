"""
Главный файл приложения FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from deribit_task.api.routers import router
from deribit_task.database import Base, engine

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Создаем приложение FastAPI
app = FastAPI(
    title="Deribit Price API",
    description="API для получения цен криптовалют с биржи Deribit",
    version="1.0.0"
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(router)


@app.get("/")
def root():
    """
    Корневой endpoint
    """
    return {
        "message": "Deribit Price API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}
