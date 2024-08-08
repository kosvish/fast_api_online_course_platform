from app.db.models.base import Base, str_200
from sqlalchemy.orm import Mapped, relationship
from .mixins import RelationMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .course_user_association_table import CourseUserAssociation
    from .users import User


class Course(Base, RelationMixin):
    _user_back_populates = "courses"
    _user_unique = True
    title: Mapped[str_200]
    description: Mapped[str_200 | None] = None
    code_language: Mapped[str_200]
    # participants_course
    users: Mapped[list["User"]] = relationship(
        back_populates="courses", secondary="course_user_association"
    )
    users_detail: Mapped[list["CourseUserAssociation"]] = relationship(
        back_populates="course"
    )
