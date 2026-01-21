"""
Конфигурационный модуль для приложения Deribit Task
"""
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Настройки базы данных
DB_USER = getenv('DB_USER', 'postgres')
DB_PASSWORD = getenv('DB_PASSWORD', 'postgres')
DB_NAME = getenv('DB_NAME', 'deribit_db')
DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', '5432')

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Настройки Celery
CELERY_BROKER_URL = getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Настройки Deribit API
DERIBIT_API_URL = 'https://www.deribit.com/api/v2'

# Поддерживаемые тикеры
SUPPORTED_TICKERS = ['BTC_USD', 'ETH_USD']
