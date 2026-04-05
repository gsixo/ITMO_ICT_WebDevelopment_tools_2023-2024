from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


async def get_transaction(db: AsyncSession, transaction_id: int) -> Transaction | None:
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    return result.scalar_one_or_none()


async def get_transactions(
    db: AsyncSession,
    account_id: int | None = None,
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Transaction]:
    stmt = select(Transaction).offset(skip).limit(limit)
    if account_id is not None:
        stmt = stmt.where(Transaction.account_id == account_id)
    if category_id is not None:
        stmt = stmt.where(Transaction.category_id == category_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_transaction_with_relations(db: AsyncSession, transaction_id: int) -> Transaction | None:
    result = await db.execute(
        select(Transaction)
        .options(
            selectinload(Transaction.account),
            selectinload(Transaction.category),
        )
        .where(Transaction.id == transaction_id)
    )
    return result.scalar_one_or_none()


async def create_transaction(db: AsyncSession, data: TransactionCreate) -> Transaction:
    transaction = Transaction(**data.model_dump())
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


async def update_transaction(
    db: AsyncSession, transaction_id: int, data: TransactionUpdate
) -> Transaction | None:
    transaction = await get_transaction(db, transaction_id)
    if transaction is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(transaction, field, value)
    await db.commit()
    await db.refresh(transaction)
    return transaction


async def delete_transaction(db: AsyncSession, transaction_id: int) -> bool:
    transaction = await get_transaction(db, transaction_id)
    if transaction is None:
        return False
    await db.delete(transaction)
    await db.commit()
    return True
