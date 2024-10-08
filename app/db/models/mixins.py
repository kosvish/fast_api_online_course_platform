from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User


class RelationMixin:
    _user_unique: bool = False
    _user_nullable: bool = False
    _user_back_populates: str | None = None

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User", back_populates=cls._user_back_populates)

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey('users.id'), unique=cls._user_unique, nullable=cls._user_nullable
        )