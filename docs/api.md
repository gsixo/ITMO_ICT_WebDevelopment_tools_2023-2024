# API

Базовый URL: `http://localhost:8000`

Полная интерактивная документация: [Swagger UI](http://localhost:8000/docs)

## Обзор ресурсов

| Префикс | Ресурс | Описание |
|---------|--------|----------|
| `/persons` | Пользователи | Владельцы счетов и финансовых данных |
| `/accounts` | Счета | Банковские/наличные счета пользователя |
| `/categories` | Категории | Категории доходов и расходов |
| `/transactions` | Транзакции | Операции по счетам |
| `/budgets` | Бюджеты | Лимиты расходов по категориям |
| `/goals` | Цели | Финансовые цели накопления |
| `/notifications` | Уведомления | Уведомления пользователю |
| `/health` | Health | Проверка работоспособности |

## Общие паттерны

Для каждого ресурса (кроме `/health`) реализованы стандартные операции:

| Метод | Путь | Действие |
|-------|------|----------|
| `POST` | `/` | Создание |
| `GET` | `/` | Список (с `skip`, `limit`) |
| `GET` | `/{id}` | Получение по ID |
| `PUT` | `/{id}` | Полное обновление |
| `PATCH` | `/{id}` | Частичное обновление |
| `DELETE` | `/{id}` | Удаление |

## Persons — `/persons`

### Создание пользователя

```bash
curl -X POST "http://localhost:8000/persons/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван Петров", "email": "ivan@example.com"}'
```

### Получение с вложенными счетами

```bash
curl "http://localhost:8000/persons/1/full"
```

## Accounts — `/accounts`

Счёт привязан к пользователю (`person_id`).

```bash
curl -X POST "http://localhost:8000/accounts/" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": 1,
    "name": "Основной счёт",
    "balance": "10000.00",
    "currency": "RUB"
  }'
```

## Categories — `/categories`

```bash
curl -X POST "http://localhost:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Продукты", "type": "expense"}'
```

Тип категории: `income` или `expense`.

## Transactions — `/transactions`

```bash
curl -X POST "http://localhost:8000/transactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 1,
    "category_id": 1,
    "store": "Пятёрочка",
    "amount": "450.00",
    "type": "expense",
    "transaction_date": "2024-05-01",
    "description": "Продукты на неделю"
  }'
```

## Budgets — `/budgets`

```bash
curl -X POST "http://localhost:8000/budgets/" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": 1,
    "category_id": 1,
    "amount_limit": "15000.00",
    "period_start": "2024-05-01",
    "period_end": "2024-05-31"
  }'
```

## Goals — `/goals`

```bash
curl -X POST "http://localhost:8000/goals/" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": 1,
    "name": "Отпуск",
    "target_amount": "100000.00",
    "current_amount": "25000.00",
    "deadline": "2024-12-01"
  }'
```

## Notifications — `/notifications`

```bash
curl -X POST "http://localhost:8000/notifications/" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": 1,
    "title": "Превышен бюджет",
    "message": "Расходы по категории Продукты превысили лимит",
    "is_read": false
  }'
```

## Коды ответов

| Код | Значение |
|-----|----------|
| `200` | Успешный запрос |
| `201` | Ресурс создан |
| `204` | Ресурс удалён |
| `404` | Ресурс не найден |
| `422` | Ошибка валидации входных данных |
