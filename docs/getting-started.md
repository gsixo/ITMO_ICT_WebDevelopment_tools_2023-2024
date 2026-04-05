# Быстрый старт

## Требования

- Python 3.11+
- PostgreSQL 14+ (локально или в Docker)

## 1. Клонирование репозитория

```bash
git clone <repo-url>
cd ITMO_ICT_WebDevelopment_tools_2023-2024
git checkout lab1
```

## 2. Виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Переменные окружения

```bash
cp .env.example .env
```

Для локального запуска без Docker раскомментируйте в `.env` строки с `localhost`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/finance_db
DATABASE_URL_SYNC=postgresql+psycopg2://user:password@localhost:5432/finance_db
```

Замените `user`, `password` и имя базы на свои значения.

## 4. Создание базы данных

```bash
sudo -u postgres psql -c "CREATE DATABASE finance_db;"
```

## 5. Миграции

```bash
alembic upgrade head
```

При изменении моделей:

```bash
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
```

## 6. Запуск приложения

```bash
uvicorn app:app --reload
```

| URL | Назначение |
|-----|------------|
| [http://localhost:8000](http://localhost:8000) | API |
| [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI |
| [http://localhost:8000/redoc](http://localhost:8000/redoc) | ReDoc |
| [http://localhost:8000/health](http://localhost:8000/health) | Health-check |

## 7. Документация MkDocs

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Сайт документации откроется на [http://127.0.0.1:8000](http://127.0.0.1:8000) — если порт занят API, укажите другой:

```bash
mkdocs serve -a 127.0.0.1:8002
```

## Пример запроса

```bash
curl -X POST "http://localhost:8000/persons/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван", "email": "ivan@example.com"}'
```
