from sqlalchemy import ForeignKey
from typing import Annotated, Optional

from .base import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column


class Courses(Base):
    __tablename__ = "courses"
    title: Mapped[str_200]
    description: Mapped[str_200 | None] = None
    code_language: Mapped[str_200]
    mentor: Mapped[str_200]


class Books(Base):
    __tablename__ = "books"
    title: Mapped[str_200]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
