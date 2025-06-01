from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from database.db import Base  # твоя база
from database.models import *  # все модели импортируешь сюда

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # отслеживает изменения типов
        )
        with context.begin_transaction():
            context.run_migrations()

    import asyncio
    asyncio.run(
        connectable.connect().run_sync(do_migrations)
    )

run_migrations_online()
