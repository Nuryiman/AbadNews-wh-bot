from typing import Optional

from sqlalchemy import String, Integer, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from database.db import Base, AsyncSessionLocal  # Импортируем Base из db.py


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    memory: Mapped[str] = mapped_column(Text, default="")

