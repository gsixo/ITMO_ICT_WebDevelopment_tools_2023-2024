# Задача 1 — подсчёт суммы

Подсчитать сумму чисел от **1** до **1 000 000**, разбив диапазон на **4** части и выполнив их параллельно.

## Постановка

| Параметр | Значение |
|----------|----------|
| Диапазон | 1 … 1 000 000 |
| Workers | 4 |
| Ожидаемый результат | 500 000 500 000 |

Функция `calculate_sum(start, end)` считает `sum(range(start, end + 1))`.

## Реализации

### Threading — `task1_threading.py`

```mermaid
flowchart TB
    Main["Главный поток"] --> T1["Thread 1"]
    Main --> T2["Thread 2"]
    Main --> T3["Thread 3"]
    Main --> T4["Thread 4"]
    T1 --> R["results[]"]
    T2 --> R
    T3 --> R
    T4 --> R
    R --> Sum["sum(results)"]
```

- Модуль `threading`, по одному потоку на диапазон
- Общий список `results` в памяти процесса
- `thread.join()` — ожидание завершения

### Multiprocessing — `task1_multiprocessing.py`

```mermaid
flowchart TB
    Main["Главный процесс"] --> Pool["Pool(4)"]
    Pool --> P1["Процесс 1"]
    Pool --> P2["Процесс 2"]
    Pool --> P3["Процесс 3"]
    Pool --> P4["Процесс 4"]
    P1 --> Map["pool.map()"]
    P2 --> Map
    P3 --> Map
    P4 --> Map
    Map --> Sum["sum(partial_sums)"]
```

- `multiprocessing.Pool` с `pool.map`
- Каждый процесс — отдельная память, обход GIL для CPU-задач

### Async — `task1_async.py`

```mermaid
flowchart TB
    Main["asyncio.run()"] --> G["asyncio.gather()"]
    G --> C1["coroutine 1"]
    G --> C2["coroutine 2"]
    G --> C3["coroutine 3"]
    G --> C4["coroutine 4"]
    C1 --> Sleep["await asyncio.sleep(0)"]
    C2 --> Sleep
    C3 --> Sleep
    C4 --> Sleep
    Sleep --> Calc["calculate_sum()"]
```

- `async def` + `asyncio.gather`
- `await asyncio.sleep(0)` — точка уступки event loop
- **Не ускоряет CPU-bound**: `calculate_sum` блокирует event loop

## Запуск

```bash
python task1_threading.py
python task1_multiprocessing.py
python task1_async.py
```

Время записывается в `results/task1_times.csv`.

## Выводы

| Подход | CPU-bound задача | Почему |
|--------|------------------|--------|
| **threading** | Слабое ускорение | GIL — только один поток выполняет Python-байткод |
| **multiprocessing** | Лучшее ускорение | Отдельные процессы, каждый со своим GIL |
| **async** | Почти без ускорения | Кооперативность не помогает при чистых вычислениях |

Для **I/O-bound** задач (задача 2) картина меняется — см. [Задача 2](task2.md).
