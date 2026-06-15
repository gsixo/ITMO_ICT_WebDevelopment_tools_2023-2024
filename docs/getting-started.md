# Быстрый старт

## Требования

- Python 3.11+
- Docker и Docker Compose (рекомендуется)
- PostgreSQL и Redis (при локальном запуске)

## Установка

```bash
git clone https://github.com/gsixo/ITMO_ICT_WebDevelopment_tools_2023-2024
cd ITMO_ICT_WebDevelopment_tools_2023-2024
git checkout lab3

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Вариант A: Docker Compose (рекомендуется)

```bash
docker compose up --build
```

| Сервис | URL |
|--------|-----|
| Finance API | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Parser Service | [http://localhost:8001/docs](http://localhost:8001/docs) |
| PostgreSQL (host) | `localhost:5433` |
| Redis (host) | `localhost:6379` |

Миграции применяются автоматически при старте контейнера `api`.

## Вариант B: локальный запуск

Нужны PostgreSQL и Redis. В `.env` для Docker-имён (`db`, `parser`, `redis`) — `runtime_env.py` перепишет их в `localhost` при запуске на хосте.

```bash
docker compose up -d db redis   # только инфраструктура
alembic upgrade head
```

Три терминала:

```bash
# 1. API
uvicorn app.main:app --reload

# 2. Parser
uvicorn parser_service.main:app --host 0.0.0.0 --port 8001 --reload

# 3. Celery worker (для /parser/parse-async)
celery -A app.celery_app:celery_app worker --loglevel=info
```

## Проверка парсинга

### Синхронно через API

```bash
curl -X POST "http://localhost:8000/parser/parse" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","workers":4}'
```

### Асинхронно через Celery

```bash
curl -X POST "http://localhost:8000/parser/parse-async" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

curl "http://localhost:8000/parser/tasks/<task_id>"
```

### Результаты в БД

```bash
psql "postgresql://postgres:postgres@localhost:5433/finance_db" -c \
  "SELECT id, approach, url, title, fetched_at FROM parsed_pages ORDER BY fetched_at DESC LIMIT 10;"
```

## Документация MkDocs

```bash
pip install -r requirements-docs.txt
mkdocs serve -a 127.0.0.1:8002
```
