from .base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UniqueConstraint, ForeignKey


class CourseUserAssociation(Base):
    __tablename__ = "course_user_association"
    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "user_id",
            name="idx_unique_course_user",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    count_participants: Mapped[int] = mapped_column(default=0, server_default="0")
