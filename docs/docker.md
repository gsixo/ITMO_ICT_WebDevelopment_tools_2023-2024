# Docker

Проект можно запустить целиком через **Docker Compose**: API, PostgreSQL, Redis, parser-сервис и Celery worker.

## Сервисы

```mermaid
flowchart TB
    subgraph compose["Docker Compose"]
        API["api :8000"]
        Parser["parser :8001"]
        Worker["celery_worker"]
        DB[("db\nPostgreSQL")]
        Redis[("redis")]
    end

    API --> DB
    API --> Parser
    API --> Redis
    Worker --> DB
    Worker --> Redis
```

| Сервис | Порт (host) | Назначение |
|--------|-------------|------------|
| `api` | 8000 | FastAPI приложение |
| `parser` | 8001 | HTTP-сервис парсера |
| `db` | — | PostgreSQL (внутренняя сеть) |
| `redis` | — | Брокер Celery |
| `celery_worker` | — | Фоновые задачи |

## Быстрый запуск

```bash
docker compose up --build
```

После старта:

- API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Parser: [http://localhost:8001/docs](http://localhost:8001/docs)

Сервис `api` автоматически выполняет `alembic upgrade head` перед запуском Uvicorn.

## Переменные окружения

В `docker-compose.yml` заданы через YAML-якорь `x-app-environment`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/finance_db
DATABASE_URL_SYNC=postgresql+psycopg2://postgres:postgres@db:5432/finance_db
PARSER_SERVICE_URL=http://parser:8001
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

Внутри Docker-сети сервисы обращаются друг к другу по именам: `db`, `parser`, `redis`.

## Локальный запуск + Docker БД

Если API запускается на хосте, а PostgreSQL — в Docker, раскомментируйте в `docker-compose.yml` проброс порта:

```yaml
db:
  ports:
    - "5433:5432"
```

И укажите в `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/finance_db
DATABASE_URL_SYNC=postgresql+psycopg2://postgres:postgres@localhost:5433/finance_db
```

## Полезные команды

```bash
# Запуск в фоне
docker compose up -d

# Только БД и Redis
docker compose up -d db redis

# Логи
docker compose logs -f api

# Остановка
docker compose down

# Остановка с удалением тома БД
docker compose down -v
```

## Dockerfile

Корневой `Dockerfile` собирает образ API и Celery worker:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Parser-сервис собирается из `parser/Dockerfile`.

## Сборка документации в CI

Статический сайт MkDocs можно собрать в Docker или локально:

```bash
pip install -r requirements-docs.txt
mkdocs build
# результат в site/
```

Папка `site/` добавлена в `.gitignore`.
