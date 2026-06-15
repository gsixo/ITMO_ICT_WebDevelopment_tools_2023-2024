# Launch Instructions

## Prerequisites

- Python 3.11+
- PostgreSQL (running locally or remotely)
- Docker and Docker Compose (for containerized run)

## 1. Clone the repository

```bash
git clone <repo-url>
cd ITMO_ICT_WebDevelopment_tools_2023-2024
git checkout <your-branch>
```

## 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure environment variables

Copy the example file and fill in your database credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/finance_db
DATABASE_URL_SYNC=postgresql+psycopg2://user:password@localhost:5432/finance_db
PARSER_SERVICE_URL=http://localhost:8001
PARSER_SERVICE_TIMEOUT_SECONDS=30
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

Replace `user`, `password`, and `finance_db` with your actual PostgreSQL credentials.

## 4. Create the database

```bash
  sudo -u postgres psql -c "CREATE DATABASE finance_db;" 
```

## 5. Apply migrations

###  Alembic

```bash
alembic revision --autogenerate -m "initial"                                                                             
alembic upgrade head
```

## 6. Run the application

### Main API

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Parser service (separate HTTP app)

```bash
uvicorn parser_service.main:app --host 0.0.0.0 --port 8001 --reload
```

Parser service docs: [http://localhost:8001/docs](http://localhost:8001/docs)

### Celery worker (for async parser queue)

```bash
celery -A app.celery_app:celery_app worker --loglevel=info
```

## 7. HTTP parser flow

### Call parser directly

```bash
curl -X POST "http://localhost:8001/parse" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","workers":4}'
```

### Call parser through main API proxy endpoint

```bash
curl -X POST "http://localhost:8000/parser/parse" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","workers":4}'
```

### Queue async parse task via Celery

```bash
curl -X POST "http://localhost:8000/parser/parse-async" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Then poll task status:

```bash
curl "http://localhost:8000/parser/tasks/<task_id>"
```

## 8. Docker Compose

Start all services (`db`, `redis`, `parser`, `api`, `celery_worker`) with one command:

```bash
docker compose up --build
docker compose exec api alembic upgrade head

```

Services:
- Main API: [http://localhost:8000](http://localhost:8000)
- Parser service: [http://localhost:8001](http://localhost:8001)
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## 9. Verify saved parsing results in DB

```bash
psql "postgresql://postgres:postgres@localhost:5432/finance_db" \
  -c "SELECT id, approach, url, title, fetched_at FROM parsed_pages ORDER BY fetched_at DESC LIMIT 20;"
```

## API Overview

| Prefix           | Resource      |
|------------------|---------------|
| `/persons`       | Users         |
| `/accounts`      | Accounts      |
| `/categories`    | Categories    |
| `/transactions`  | Transactions  |
| `/budgets`       | Budgets       |
| `/goals`         | Goals         |
| `/notifications` | Notifications |
| `/parser`        | Parser proxy  |

## MkDocs documentation

```bash
pip install -r requirements-docs.txt
mkdocs serve -a 127.0.0.1:8002
```

GitHub Pages: [lab1](https://gsixo.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/lab1/) · [lab2](https://gsixo.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/lab2/) · [lab3](https://gsixo.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/lab3/) — Settings → Pages → branch `gh-pages`.
