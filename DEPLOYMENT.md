# Инструкция по разворачиванию

## Быстрый старт с Docker Compose (рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone <repository_url>
cd deribit_task
```

2. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

3. При необходимости отредактируйте `.env` (по умолчанию настройки подходят для Docker Compose)

4. Запустите все сервисы:
```bash
docker-compose up -d
```

5. Примените миграции базы данных:
```bash
docker-compose exec api alembic upgrade head
```

6. Проверьте статус сервисов:
```bash
docker-compose ps
```

7. API будет доступно по адресу: http://localhost:8000/docs

## Локальная установка (без Docker)

### Требования:
- Python 3.11+
- PostgreSQL 16+
- Redis

### Шаги:

1. Клонируйте репозиторий:
```bash
git clone <repository_url>
cd deribit_task
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env`:
```bash
cp env.example .env
```

5. Настройте переменные окружения в `.env`:
```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=deribit_db
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

6. Создайте базу данных PostgreSQL:
```bash
createdb deribit_db
# или через psql:
# psql -U postgres
# CREATE DATABASE deribit_db;
```

7. Примените миграции:
```bash
alembic upgrade head
```

8. Запустите Redis (если еще не запущен):
```bash
redis-server
```

9. В отдельном терминале запустите Celery worker:
```bash
celery -A deribit_task.celery_app worker --loglevel=info
```

10. В еще одном терминале запустите Celery beat:
```bash
celery -A deribit_task.celery_app beat --loglevel=info
```

11. Запустите FastAPI приложение:
```bash
uvicorn deribit_task.main:app --host 0.0.0.0 --port 8000
```

12. API будет доступно по адресу: http://localhost:8000/docs

## Проверка работы

После запуска проверьте:

1. Health check endpoint:
```bash
curl http://localhost:8000/health
```

2. Получение всех цен (после того, как Celery соберет данные):
```bash
curl "http://localhost:8000/api/v1/prices/all?ticker=BTC_USD"
```

3. Получение последней цены:
```bash
curl "http://localhost:8000/api/v1/prices/latest?ticker=BTC_USD"
```

## Запуск тестов

```bash
pytest deribit_task/tests/
```

## Остановка Docker Compose

```bash
docker-compose down
```

Для полной очистки (включая volumes):
```bash
docker-compose down -v
```
