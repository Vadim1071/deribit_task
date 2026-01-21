"""
Точка входа для запуска Celery worker
"""
from deribit_task.celery_app import celery_app

if __name__ == '__main__':
    celery_app.start()
