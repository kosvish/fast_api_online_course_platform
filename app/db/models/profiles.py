from sqlalchemy import Text

from app.db.models.base import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING
from .mixins import RelationMixin
if TYPE_CHECKING:
    pass


class Profile(Base, RelationMixin):
    _user_unique = True
    _user_nullable = False
    first_name: Mapped[str_200]
    last_name: Mapped[str_200]
    bio: Mapped[str] = mapped_column(Text(length=500))

