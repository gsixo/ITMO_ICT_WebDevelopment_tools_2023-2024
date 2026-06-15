# Docker

## Сервисы

```text
┌─────────┐     ┌─────────┐     ┌──────────────┐
│  api    │────▶│ parser  │     │ celery_worker│
│  :8000  │     │  :8001  │     │              │
└────┬────┘     └────┬────┘     └──────┬───────┘
     │               │                    │
     └───────────────┼────────────────────┘
                     ▼
              ┌─────────────┐      ┌───────┐
              │ PostgreSQL  │      │ Redis │
              │  db :5433   │      │ :6379 │
              └─────────────┘      └───────┘
```

## Запуск

```bash
docker compose up --build
```

Фоновый режим:

```bash
docker compose up -d --build
docker compose logs -f api
```

## Порты на хосте

| Сервис | Порт | Примечание |
|--------|------|------------|
| `api` | 8000 | Finance API |
| `parser` | 8001 | Parser service |
| `db` | 5433 | 5433→5432, чтобы не конфликтовать с локальным PostgreSQL |
| `redis` | 6379 | Celery broker |

## Переменные окружения

Заданы в `docker-compose.yml` для сервисов `api`, `parser`, `celery_worker`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/finance_db
DATABASE_URL_SYNC=postgresql+psycopg2://postgres:postgres@db:5432/finance_db
PARSER_SERVICE_URL=http://parser:8001
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

Файл `.env.example` — шаблон для локального запуска.

## Dockerfile

**`docker/api.Dockerfile`** — образ для `api` и `celery_worker`:

- Python 3.11-slim
- `requirements.txt`
- Команда по умолчанию: `uvicorn app.main:app`

**`docker/parser.Dockerfile`** — образ parser-сервиса:

- Тот же контекст (корень репо)
- Запуск: `uvicorn parser_service.main:app --port 8001`

## Полезные команды

```bash
# Миграции вручную
docker compose exec api alembic upgrade head

# Shell в контейнере API
docker compose exec api bash

# Остановка
docker compose down

# Удаление тома БД
docker compose down -v
```

## Локальный запуск + Docker-инфраструктура

```bash
docker compose up -d db redis
# .env с @db:5432 — runtime_env перепишет в localhost:5433
uvicorn app.main:app --reload
uvicorn parser_service.main:app --port 8001 --reload
celery -A app.celery_app:celery_app worker --loglevel=info
```

## Troubleshooting

| Проблема | Решение |
|----------|---------|
| `could not translate host name "db"` | Запуск на хосте без `runtime_env` — обновите код или используйте `localhost:5433` в `.env` |
| Порт 5432 занят | В compose уже используется `5433:5432` |
| Celery `PENDING` | Запустите `celery_worker` или локальный worker |
| Порт 8001 занят | Остановите старый parser или используйте только Docker |
