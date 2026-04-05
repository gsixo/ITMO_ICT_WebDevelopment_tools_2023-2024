# Launch Instructions

## Prerequisites

- Python 3.11+
- PostgreSQL (running locally or remotely)

## 1. Clone the repository

```bash
git clone <repo-url>
cd ITMO_ICT_WebDevelopment_tools_2023-2024
git checkout lab2
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

```bash
psql "postgresql://gsixo:strongpassword@localhost:5432/finance_db"

SELECT id, approach, url, title, fetched_at
FROM parsed_pages
ORDER BY fetched_at DESC
LIMIT 20;
```
