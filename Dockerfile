# Базовый образ
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы конфигурации
COPY pyproject.toml poetry.lock README.md ./

# Устанавливаем только зависимости
RUN poetry install --no-root

# Копируем код
COPY . .

# Устанавливаем модули
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
