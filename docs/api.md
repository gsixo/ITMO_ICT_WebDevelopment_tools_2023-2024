# API

Базовый URL: `http://localhost:8000`

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Finance API (lab1)

| Префикс | Ресурс |
|---------|--------|
| `/persons` | Пользователи |
| `/accounts` | Счета |
| `/categories` | Категории |
| `/transactions` | Транзакции |
| `/budgets` | Бюджеты |
| `/goals` | Цели |
| `/notifications` | Уведомления |
| `/health` | Health-check |

Стандартные CRUD: `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `PATCH /{id}`, `DELETE /{id}`.

## Parser API (lab3)

Префикс: `/parser`

### `POST /parser/parse` — синхронный парсинг

Проксирует запрос в parser-сервис, ждёт результат.

**Тело запроса:**

```json
{
  "url": "https://example.com",
  "workers": 4
}
```

или `"urls": ["https://a.com", "https://b.com"]`.

```bash
curl -X POST "http://localhost:8000/parser/parse" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","workers":4}'
```

**Ответ:** JSON с `results`, `saved`, `total`.

| Код | Причина |
|-----|---------|
| 502 | Parser service недоступен |
| 4xx/5xx | Ошибка parser-сервиса (проксируется) |

### `POST /parser/parse-async` — фоновый парсинг

Ставит задачу в очередь Celery, сразу возвращает `task_id`.

```bash
curl -X POST "http://localhost:8000/parser/parse-async" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

**Ответ:**

```json
{
  "message": "Parsing task queued",
  "task_id": "uuid...",
  "status": "QUEUED",
  "total_urls": 1
}
```

| Код | Причина |
|-----|---------|
| 503 | Redis недоступен или Celery worker не запущен |

### `GET /parser/tasks/{task_id}` — статус задачи

```bash
curl "http://localhost:8000/parser/tasks/<task_id>"
```

| status | Значение |
|--------|----------|
| `PENDING` | В очереди или неизвестный id |
| `STARTED` | Выполняется |
| `SUCCESS` | Готово, в ответе `results` |
| `FAILURE` | Ошибка в поле `error` |

## Parser Service (напрямую)

URL: `http://localhost:8001`

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/health` | Health-check |
| `POST` | `/parse` | Парсинг URL (multiprocessing) |

```bash
curl -X POST "http://localhost:8001/parse" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","workers":4}'
```

## Пример: создание пользователя

```bash
curl -X POST "http://localhost:8000/persons/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван", "email": "ivan@example.com"}'
```
