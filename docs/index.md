# Finance API

Серверное приложение для учёта личных финансов, реализованное на **FastAPI** в рамках лабораторной работы 1.

## Возможности

- CRUD для пользователей, счетов, категорий, транзакций, бюджетов, целей и уведомлений
- Асинхронная работа с PostgreSQL через SQLAlchemy 2.x и `asyncpg`
- Миграции схемы БД через Alembic
- Интерактивная документация OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Упаковка в Docker и оркестрация через Docker Compose

## Стек технологий

| Компонент | Технология |
|-----------|------------|
| Web-фреймворк | FastAPI |
| ORM | SQLAlchemy 2.x (async) |
| БД | PostgreSQL |
| Миграции | Alembic |
| Валидация | Pydantic v2 |
| Контейнеризация | Docker, Docker Compose |

## Структура документации

| Раздел | Содержание |
|--------|------------|
| [Быстрый старт](getting-started.md) | Установка, настройка `.env`, запуск |
| [Архитектура](architecture.md) | Структура проекта и слои приложения |
| [API](api.md) | Описание REST-эндпоинтов |
| [База данных](database.md) | Модели и связи между сущностями |
| [Docker](docker.md) | Запуск через Docker Compose |

## Быстрый запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app:app --reload
```

## Сборка документации

```bash
pip install -r requirements-docs.txt
mkdocs serve -a 127.0.0.1:8002
mkdocs build
```

### GitHub Pages

Каждая ветка (`lab1`, `lab2`, `lab3`) публикуется **отдельной версией** через [mike](https://github.com/jimporter/mike):

| Ветка | URL |
|-------|-----|
| lab1 | […/lab1/](https://gsixo.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/lab1/) |
| lab2 | […/lab2/](https://gsixo.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/lab2/) |
| lab3 | […/lab3/](https://gsixo.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/lab3/) |

Переключение версий — в выпадающем меню на сайте.

**Настройка (один раз):** Settings → Pages → Source → **Deploy from branch** → `gh-pages` → `/ (root)`.

После push в `lab1` и `lab2` обе документации будут доступны одновременно.
