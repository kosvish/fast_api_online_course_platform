from sqlalchemy import ForeignKey
from app.db.models.base import Base, str_200
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .course_rating_association import CourseRatingAssociation


class Course(Base):
    title: Mapped[str_200]
    description: Mapped[str | None]
    code_language: Mapped[str]
    price: Mapped[int | None] = mapped_column(default=0, server_default="0")
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    participants: Mapped[list["User"]] = relationship(
        back_populates="enrolled_course", secondary="course_user_association"
    )
    image_path: Mapped[str] = mapped_column(
        nullable=True,
        default="/course_images/courses-1.jpg",
        server_default="/course_images/courses-1.jpg",
    )
    creator: Mapped["User"] = relationship(back_populates="created_courses")

    rating_users: Mapped[list["CourseRatingAssociation"]] = relationship(
        back_populates="course", cascade="all, delete"
    )
    mean_rating: Mapped[float] = mapped_column(default=0.0, server_default="0.0")
