# База данных

Приложение использует **PostgreSQL**. Схема описана SQLAlchemy-моделями в `app/models/` и управляется через **Alembic**.

## ER-диаграмма

```mermaid
erDiagram
    persons ||--o{ accounts : has
    persons ||--o{ budgets : has
    persons ||--o{ goals : has
    persons ||--o{ notifications : has
    accounts ||--o{ transactions : has
    categories ||--o{ transactions : has
    categories ||--o{ budgets : has

    persons {
        int id PK
        string name
        string email UK
        datetime created_at
        datetime updated_at
    }

    accounts {
        int id PK
        int person_id FK
        string name
        decimal balance
        string currency
        datetime created_at
    }

    categories {
        int id PK
        string name
        enum type
        datetime created_at
    }

    transactions {
        int id PK
        int account_id FK
        int category_id FK
        string store
        decimal amount
        enum type
        date transaction_date
        text description
        datetime created_at
    }

    budgets {
        int id PK
        int person_id FK
        int category_id FK
        decimal amount_limit
        date period_start
        date period_end
        datetime created_at
    }

    goals {
        int id PK
        int person_id FK
        string name
        decimal target_amount
        decimal current_amount
        date deadline
        datetime created_at
    }

    notifications {
        int id PK
        int person_id FK
        string title
        text message
        bool is_read
        datetime created_at
    }
```

## Таблицы

### `persons`

Пользователь системы — владелец счетов и финансовых данных.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Первичный ключ |
| `name` | VARCHAR(255) | Имя |
| `email` | VARCHAR(255) | Email (уникальный) |
| `created_at` | TIMESTAMP | Дата создания |
| `updated_at` | TIMESTAMP | Дата обновления |

### `accounts`

Финансовый счёт пользователя.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Первичный ключ |
| `person_id` | INTEGER | FK → `persons.id` |
| `name` | VARCHAR(255) | Название счёта |
| `balance` | NUMERIC(15,2) | Текущий баланс |
| `currency` | VARCHAR(3) | Валюта (RUB, USD, …) |

### `categories`

Категории доходов и расходов.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Первичный ключ |
| `name` | VARCHAR(255) | Название |
| `type` | ENUM | `income` или `expense` |

### `transactions`

Финансовая операция по счёту.

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Первичный ключ |
| `account_id` | INTEGER | FK → `accounts.id` |
| `category_id` | INTEGER | FK → `categories.id` |
| `store` | VARCHAR(255) | Магазин / источник |
| `amount` | NUMERIC(15,2) | Сумма |
| `type` | ENUM | `income` или `expense` |
| `transaction_date` | DATE | Дата операции |
| `description` | TEXT | Комментарий |

### `budgets`

Бюджет — лимит расходов по категории за период.

| Поле | Тип | Описание |
|------|-----|----------|
| `person_id` | INTEGER | FK → `persons.id` |
| `category_id` | INTEGER | FK → `categories.id` |
| `amount_limit` | NUMERIC(15,2) | Лимит |
| `period_start` | DATE | Начало периода |
| `period_end` | DATE | Конец периода |

### `goals`

Финансовая цель накопления.

| Поле | Тип | Описание |
|------|-----|----------|
| `person_id` | INTEGER | FK → `persons.id` |
| `name` | VARCHAR(255) | Название цели |
| `target_amount` | NUMERIC(15,2) | Целевая сумма |
| `current_amount` | NUMERIC(15,2) | Накоплено |
| `deadline` | DATE | Срок |

### `notifications`

Уведомления пользователю.

| Поле | Тип | Описание |
|------|-----|----------|
| `person_id` | INTEGER | FK → `persons.id` |
| `title` | VARCHAR(255) | Заголовок |
| `message` | TEXT | Текст |
| `is_read` | BOOLEAN | Прочитано |

## Миграции

Исходные SQL-скрипты: `script/migrations/`.

Alembic-миграции: `alembic/versions/`.

```bash
# Применить все миграции
alembic upgrade head

# Откатить последнюю
alembic downgrade -1

# Создать новую миграцию после изменения моделей
alembic revision --autogenerate -m "add field"
```

## Подключение

| Режим | URL |
|-------|-----|
| Async (приложение) | `postgresql+asyncpg://user:pass@host:5432/finance_db` |
| Sync (Alembic) | `postgresql+psycopg2://user:pass@host:5432/finance_db` |

Переменные задаются в `.env`: `DATABASE_URL`, `DATABASE_URL_SYNC`.
