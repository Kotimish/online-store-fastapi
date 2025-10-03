## Веб-приложение на FastAPI

### Установка

1. **Клонируем репозиторий и переходим в папку проекта**
    - По HTTP
    ```bash
    git clone https://github.com/Kotimish/online-store-fastapi
    ```
   - Или по SSH
    ```bash
    git clone git@github.com:Kotimish/online-store-fastapi.git
    ```
    - Переходим в созданную папку проекта
    ```bash
    cd online-store-fastapi
    ```
2. **Создаем виртуальное окружение**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    PS: Убедитесь, что ваша версия Python не ниже 3.12
    При необходимости указывайте явно версию Python при создании окружения
    К примеру (для Python3.12)
    ```bash
    python3.12 -m venv .venv
    source .venv/bin/activate
    ```
3. **Устанавливаем необходимые пакеты с помощью requirements.txt**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Запуск приложения**
    ```bash
    python app.py
    ```
    Или
    ```bash
    uvicorn app:app --host=127.0.0.1 --port=8000 --reload=True
    ```
