from sqlalchemy import ForeignKey

from app.db.models.base import Base, str_200
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .mixins import RelationMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .course_user_association_table import CourseUserAssociation
    from .users import User


class Course(Base):
    title: Mapped[str_200]
    description: Mapped[str_200 | None] = None
    code_language: Mapped[str_200]
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    participants: Mapped[list["User"]] = relationship(
        back_populates="enrolled_course", secondary="course_user_association"
    )
    creator: Mapped['User'] = relationship(back_populates='created_courses')
