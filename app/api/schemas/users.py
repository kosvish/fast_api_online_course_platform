from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr = Field(max_length=40)
    hash_password: str


class CreateUser(BaseUser):
    pass


class UpdateUser(BaseUser):
    pass


class UpdateUserPartial(UpdateUser):
    username: Optional[str | None] = None
    email: EmailStr | None = None
    hash_password: str | None


class ResponseUser(BaseModel):
    username: str
    email: EmailStr

