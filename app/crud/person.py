from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate


async def get_person(db: AsyncSession, person_id: int) -> Person | None:
    result = await db.execute(select(Person).where(Person.id == person_id))
    return result.scalar_one_or_none()


async def get_persons(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Person]:
    result = await db.execute(select(Person).offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_person_with_accounts(db: AsyncSession, person_id: int) -> Person | None:
    result = await db.execute(
        select(Person)
        .options(selectinload(Person.accounts))
        .where(Person.id == person_id)
    )
    return result.scalar_one_or_none()


async def create_person(db: AsyncSession, data: PersonCreate) -> Person:
    person = Person(**data.model_dump())
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person


async def update_person(db: AsyncSession, person_id: int, data: PersonUpdate) -> Person | None:
    person = await get_person(db, person_id)
    if person is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(person, field, value)
    await db.commit()
    await db.refresh(person)
    return person


async def delete_person(db: AsyncSession, person_id: int) -> bool:
    person = await get_person(db, person_id)
    if person is None:
        return False
    await db.delete(person)
    await db.commit()
    return True
