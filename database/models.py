from dataclasses import dataclass
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


@dataclass
class SchemaTask:
    title: str
    description: str
    status: bool


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[bool]

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, telegram_id={self.telegram_id!r})"

    def __str__(self):
        return f'{self.title} : {self.telegram_id}'
