# Быстрый старт

## Требования

- Python 3.11+
- PostgreSQL (для задачи 2)

## Установка

```bash
git clone https://github.com/gsixo/ITMO_ICT_WebDevelopment_tools_2023-2024
cd ITMO_ICT_WebDevelopment_tools_2023-2024
git checkout lab2

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## База данных (задача 2)

```bash
cp .env.example .env
```

### Вариант A: PostgreSQL в Docker

```bash
docker compose up -d db
```

В `.env` оставьте Docker-имена (`@db:5432`) — `db.py` автоматически перепишет их в `@localhost:5433` при запуске на хосте.

### Вариант B: локальный PostgreSQL

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/finance_db
DATABASE_URL_SYNC=postgresql+psycopg2://user:password@localhost:5432/finance_db
```

Таблица `parsed_pages` создаётся автоматически при первом запуске задачи 2.

## Запуск программ

### Задача 1 — без БД

```bash
python task1_threading.py
python task1_multiprocessing.py
python task1_async.py
```

Ожидаемая сумма: `500000500000`.

### Задача 2 — с БД

```bash
python task2_threading.py
python task2_multiprocessing.py
python task2_async.py
```

## Просмотр результатов в БД

```bash
psql "postgresql://postgres:postgres@localhost:5433/finance_db" -c \
  "SELECT id, approach, url, title, fetched_at FROM parsed_pages ORDER BY fetched_at DESC LIMIT 20;"
```

## Документация MkDocs

```bash
pip install -r requirements-docs.txt
mkdocs serve -a 127.0.0.1:8002
```

Сборка статики: `mkdocs build` → папка `site/`.
