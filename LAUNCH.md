# Launch Instructions

## Prerequisites

- Python 3.11+
- PostgreSQL (running locally or remotely)

## 1. Clone the repository

```bash
git clone <repo-url>
cd ITMO_ICT_WebDevelopment_tools_2023-2024
git checkout lab1
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

```bash
uvicorn app:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

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

## MkDocs documentation

```bash
pip install -r requirements-docs.txt
mkdocs serve -a 127.0.0.1:8002
```

Open [http://127.0.0.1:8002](http://127.0.0.1:8002). Build static site: `mkdocs build` → `site/`.
