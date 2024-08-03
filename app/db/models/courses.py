from ..base import Base, str_200
from sqlalchemy.orm import Mapped
from .mixins import UserRelationMixin


class Course(Base, UserRelationMixin):
    _user_back_populates = "courses"
    _user_unique = True
    title: Mapped[str_200]
    description: Mapped[str_200 | None] = None
    code_language: Mapped[str_200]
