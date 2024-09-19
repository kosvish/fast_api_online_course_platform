import os

from sqlalchemy import ForeignKey

from app.db.models.base import Base, str_200
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .mixins import RelationMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .course_user_association_table import CourseUserAssociation
    from .users import User

base_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
images_dir = os.path.join(base_dir, "course_images")


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
        default=f"{images_dir}/courses-1.jpg",
        server_default='f"{images_dir}/courses-1.jpg"',
    )
    creator: Mapped["User"] = relationship(back_populates="created_courses")
