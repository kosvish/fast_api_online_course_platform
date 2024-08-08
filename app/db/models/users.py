from app.db.models.base import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .courses import Course
    from .course_user_association_table import CourseUserAssociation


class User(Base):
    username: Mapped[str_200]
    email: Mapped[str_200] = mapped_column(unique=True, nullable=False)
    hash_password: Mapped[str_200] = mapped_column(unique=False, nullable=False)
    course_details: Mapped[list["CourseUserAssociation"]] = relationship(
        back_populates="user"
    )
    courses: Mapped[list["Course"]] = relationship(
        back_populates="users", secondary="course_user_association"
    )
