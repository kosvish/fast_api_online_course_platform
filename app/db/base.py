from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated
from sqlalchemy import String

str_200 = Annotated[str, 200]


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    typing_annotation_map = {
        str_200: String(200)
    }
