from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database.models import User

async def create_user(session: AsyncSession, phone_number: str, memory: str = "") -> User:
    user = User(phone_number=phone_number, memory=memory)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_phone(session: AsyncSession, phone_number: str) -> User | None:
    result = await session.execute(select(User).where(User.phone_number == phone_number))
    return result.scalars().first()



async def update_user_memory(session: AsyncSession, phone_number: str, new_memory: str) -> bool:
    stmt = (
        update(User).
        where(User.phone_number == phone_number).
        values(memory=new_memory).
        execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0  # True если обновлено хотя бы одно значение

async def delete_user(session: AsyncSession, phone_number: str) -> bool:
    stmt = delete(User).where(User.phone_number == phone_number)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0  # True если удалена хотя бы одна запись
