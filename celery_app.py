"""
Конфигурация Celery для периодических задач
"""
from celery import Celery
from datetime import timedelta
import logging

from deribit_task.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

logger = logging.getLogger(__name__)

# Создаем экземпляр Celery
celery_app = Celery(
    'deribit_task',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['deribit_task.tasks']
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'fetch-prices-every-minute': {
            'task': 'deribit_task.tasks.fetch_prices',
            'schedule': timedelta(minutes=1),
        },
    },
)
