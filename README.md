# Deribit Price API

Приложение для получения и хранения цен криптовалют с биржи Deribit.

## Описание

Приложение состоит из следующих компонентов:

1. **Клиент Deribit** - асинхронный клиент для получения цен BTC/USD и ETH/USD с биржи Deribit
2. **Celery задачи** - периодическое получение цен каждую минуту
3. **FastAPI API** - REST API для доступа к сохраненным данным
4. **PostgreSQL** - база данных для хранения цен

## Требования

- Python 3.11+
- PostgreSQL 16+
- Redis (для Celery)
- Docker и Docker Compose (опционально)

## Установка и запуск

### Локальная установка

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

4. Создайте файл `.env` на основе `env.example`:
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

6. Создайте базу данных:
```bash
createdb deribit_db  # или используйте psql для создания БД
```

7. Примените миграции:
```bash
alembic upgrade head
```

8. Запустите Redis (если еще не запущен):
```bash
redis-server
```

9. Запустите Celery worker:
```bash
celery -A deribit_task.celery_app worker --loglevel=info
```

10. Запустите Celery beat (в отдельном терминале):
```bash
celery -A deribit_task.celery_app beat --loglevel=info
```

11. Запустите FastAPI приложение:
```bash
uvicorn deribit_task.main:app --host 0.0.0.0 --port 8000
```

### Запуск с Docker Compose

1. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

2. Запустите все сервисы:
```bash
docker-compose up -d
```

3. Примените миграции:
```bash
docker-compose exec api alembic upgrade head
```

4. Проверьте статус сервисов:
```bash
docker-compose ps
```

5. Остановите сервисы:
```bash
docker-compose down
```

## API Документация

После запуска приложения API документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

Все endpoints требуют обязательный query-параметр `ticker` (BTC_USD или ETH_USD).

### 1. Получение всех сохраненных данных по валюте

**GET** `/api/v1/prices/all`

**Параметры:**
- `ticker` (обязательный) - Тикер валюты (BTC_USD или ETH_USD)

**Пример запроса:**
```bash
curl "http://localhost:8000/api/v1/prices/all?ticker=BTC_USD"
```

**Пример ответа:**
```json
{
  "ticker": "BTC_USD",
  "count": 2,
  "data": [
    {
      "id": 1,
      "ticker": "BTC_USD",
      "price": "50000.5",
      "timestamp": 1000000
    },
    {
      "id": 2,
      "ticker": "BTC_USD",
      "price": "51000.0",
      "timestamp": 1000060
    }
  ]
}
```

### 2. Получение последней цены валюты

**GET** `/api/v1/prices/latest`

**Параметры:**
- `ticker` (обязательный) - Тикер валюты (BTC_USD или ETH_USD)

**Пример запроса:**
```bash
curl "http://localhost:8000/api/v1/prices/latest?ticker=BTC_USD"
```

**Пример ответа:**
```json
{
  "id": 2,
  "ticker": "BTC_USD",
  "price": "51000.0",
  "timestamp": 1000060
}
```

### 3. Получение цены валюты с фильтром по дате

**GET** `/api/v1/prices/filter`

**Параметры:**
- `ticker` (обязательный) - Тикер валюты (BTC_USD или ETH_USD)
- `date_from` (опциональный) - Начальная дата в UNIX timestamp
- `date_to` (опциональный) - Конечная дата в UNIX timestamp

**Пример запроса:**
```bash
curl "http://localhost:8000/api/v1/prices/filter?ticker=BTC_USD&date_from=1000000&date_to=1000030"
```

**Пример ответа:**
```json
{
  "ticker": "BTC_USD",
  "count": 1,
  "data": [
    {
      "id": 1,
      "ticker": "BTC_USD",
      "price": "50000.5",
      "timestamp": 1000000
    }
  ]
}
```

## Запуск тестов

```bash
pytest deribit_task/tests/
```

Для запуска с покрытием:
```bash
pytest deribit_task/tests/ --cov=deribit_task --cov-report=html
```

## Структура проекта

```
deribit_task/
├── api/                    # API модуль
│   ├── __init__.py
│   ├── routers.py         # FastAPI роутеры
│   └── schemas.py         # Pydantic схемы
├── migrations/            # Alembic миграции
│   ├── env.py
│   └── versions/
├── tests/                 # Unit тесты
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_crud.py
│   └── test_deribit_client.py
├── alembic.ini            # Конфигурация Alembic
├── celery_app.py          # Конфигурация Celery
├── config.py              # Конфигурация приложения
├── crud.py                # CRUD операции
├── database.py            # Настройки БД
├── deribit_client.py      # Клиент Deribit API
├── docker-compose.yml     # Docker Compose конфигурация
├── Dockerfile             # Docker образ
├── env.example            # Пример переменных окружения
├── main.py                # Точка входа FastAPI
├── models.py              # SQLAlchemy модели
├── requirements.txt       # Зависимости Python
├── tasks.py               # Celery задачи
└── README.md              # Документация
```

## Design Decisions

### Архитектура

1. **Разделение ответственности**: Код разделен на модули по функциональности:
   - `deribit_client.py` - работа с внешним API
   - `models.py` - модели данных
   - `crud.py` - операции с БД
   - `api/routers.py` - HTTP endpoints
   - `tasks.py` - фоновые задачи

2. **Использование репозиторного паттерна**: CRUD операции вынесены в отдельный класс `PriceRepository` для упрощения тестирования и переиспользования кода.

3. **Асинхронный клиент**: Использован `aiohttp` для асинхронных HTTP запросов к Deribit API, что повышает производительность.

4. **Dependency Injection**: В FastAPI используется dependency injection для получения сессии БД, что упрощает тестирование и управление ресурсами.

### База данных

1. **PostgreSQL**: Выбрана как надежная и производительная реляционная БД для хранения временных рядов.

2. **Индексы**: Добавлены индексы на поля `ticker` и `timestamp` для оптимизации запросов по тикеру и времени.

3. **Тип данных для цены**: Использован `Numeric(precision=20, scale=8)` для точного хранения цен криптовалют без потери точности.

### Celery

1. **Периодические задачи**: Использован Celery Beat для запуска задачи каждую минуту.

2. **Брокер сообщений**: Redis выбран как легковесный и быстрый брокер для Celery.

3. **Обработка ошибок**: Задачи содержат обработку ошибок с логированием для отладки.

### API

1. **Валидация**: Все входные данные валидируются через Pydantic схемы и query-параметры FastAPI.

2. **Обработка ошибок**: Использованы HTTP исключения FastAPI для возврата понятных ошибок клиенту.

3. **Документация**: Автоматическая генерация документации через Swagger UI и ReDoc.

### Тестирование

1. **Unit тесты**: Написаны тесты для основных компонентов:
   - Клиент Deribit API
   - CRUD операции
   - API endpoints

2. **Фикстуры**: Использованы pytest фикстуры для создания тестовой БД и изоляции тестов.

3. **Моки**: Использованы моки для тестирования внешних зависимостей (HTTP запросы).

### Docker

1. **Мультиконтейнерная архитектура**: Отдельные контейнеры для:
   - API приложения
   - PostgreSQL
   - Redis
   - Celery worker
   - Celery beat

2. **Health checks**: Добавлены health checks для БД и Redis для правильной последовательности запуска.

3. **Volumes**: Использованы volumes для персистентности данных БД.

### Безопасность

1. **Переменные окружения**: Все секретные данные хранятся в переменных окружения, не коммитятся в репозиторий.

2. **Валидация входных данных**: Все входные данные валидируются перед обработкой.

3. **Обработка ошибок**: Ошибки логируются, но не раскрывают внутреннюю структуру системы.

## Мониторинг

Для мониторинга Celery задач можно использовать:
- Flower: `celery -A deribit_task.celery_app flower`
- Redis CLI: `redis-cli` для проверки очереди задач

## Логирование

Логирование настроено через стандартный модуль `logging` Python. Уровни логирования:
- INFO - информационные сообщения
- WARNING - предупреждения
- ERROR - ошибки

## Производительность

1. **Connection pooling**: SQLAlchemy использует connection pool для эффективного управления соединениями с БД.

2. **Асинхронность**: Асинхронные HTTP запросы через aiohttp повышают производительность при работе с внешним API.

3. **Индексы БД**: Индексы на часто используемых полях ускоряют запросы.

## Возможные улучшения

1. Добавить кэширование для часто запрашиваемых данных
2. Добавить пагинацию для endpoints с большим количеством данных
3. Добавить метрики и мониторинг (Prometheus, Grafana)
4. Добавить rate limiting для API
5. Добавить аутентификацию и авторизацию
6. Добавить более детальное логирование и трейсинг запросов

