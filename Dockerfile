FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Команда по умолчанию - запуск FastAPI
CMD ["uvicorn", "deribit_task.main:app", "--host", "0.0.0.0", "--port", "8000"]
