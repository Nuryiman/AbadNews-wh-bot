import asyncio

from database.db import Base, engine
from database.models import User

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_all_tables())