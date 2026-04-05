from fastapi import FastAPI

from app.routers import accounts, budgets, categories, goals, notifications, parser, persons, transactions

app = FastAPI(title="Finance API")

app.include_router(persons.router, prefix="/persons", tags=["persons"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
app.include_router(goals.router, prefix="/goals", tags=["goals"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(parser.router, prefix="/parser", tags=["parser"])


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
