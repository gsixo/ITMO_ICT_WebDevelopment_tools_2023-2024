from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.account import AccountCreate, AccountUpdate


async def get_account(db: AsyncSession, account_id: int) -> Account | None:
    result = await db.execute(select(Account).where(Account.id == account_id))
    return result.scalar_one_or_none()


async def get_accounts(
    db: AsyncSession,
    person_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Account]:
    stmt = select(Account).offset(skip).limit(limit)
    if person_id is not None:
        stmt = stmt.where(Account.person_id == person_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_account_with_transactions(db: AsyncSession, account_id: int) -> Account | None:
    result = await db.execute(
        select(Account)
        .options(
            selectinload(Account.transactions).selectinload(Transaction.category)
        )
        .where(Account.id == account_id)
    )
    return result.scalar_one_or_none()


async def create_account(db: AsyncSession, data: AccountCreate) -> Account:
    account = Account(**data.model_dump())
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


async def update_account(db: AsyncSession, account_id: int, data: AccountUpdate) -> Account | None:
    account = await get_account(db, account_id)
    if account is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(account, field, value)
    await db.commit()
    await db.refresh(account)
    return account


async def delete_account(db: AsyncSession, account_id: int) -> bool:
    account = await get_account(db, account_id)
    if account is None:
        return False
    await db.delete(account)
    await db.commit()
    return True
