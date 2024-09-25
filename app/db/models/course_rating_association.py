from app.db.models.base import Base, str_200
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .courses import Course
    from .users import User


class CourseRatingAssociation(Base):
    __tablename__ = "course_rating_association"
    __table_args__ = (
        UniqueConstraint("course_id", "user_id", name="idx_unique_course_user_rating"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))

    user: Mapped["User"] = relationship(back_populates="rated_courses")
    course: Mapped["Course"] = relationship(back_populates="rating_users")
