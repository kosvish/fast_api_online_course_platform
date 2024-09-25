from app.db.models.base import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import LargeBinary

if TYPE_CHECKING:
    from .courses import Course
    from .course_rating_association import CourseRatingAssociation


class User(Base):
    __tablename__ = "users"
    username: Mapped[str_200]
    email: Mapped[str_200] = mapped_column(unique=True, nullable=False)
    hash_password: Mapped[bytes] = mapped_column(
        LargeBinary, nullable=False, unique=False
    )
    enrolled_course: Mapped[list["Course"]] = relationship(
        back_populates="participants", secondary="course_user_association"
    )
    created_courses: Mapped[list["Course"]] = relationship(back_populates="creator")
    image_path: Mapped[str] = mapped_column(
        nullable=True,
        default="/user_images/default.jpg",
        server_default="/user_images/default.jpg",
    )

    rated_courses: Mapped[list["CourseRatingAssociation"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
