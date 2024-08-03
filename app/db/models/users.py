from ..base import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    username: Mapped[str_200]
    email: Mapped[str_200] = mapped_column(unique=True, nullable=False)
    hash_password: Mapped[str_200] = mapped_column(unique=False, nullable=False)