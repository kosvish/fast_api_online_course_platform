from typing import Optional

from fastapi import Form, UploadFile, File
from pydantic import BaseModel, EmailStr, Field, ConfigDict


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
    hash_password: str | None = None


class ResponseUser(BaseModel):
    username: str
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    email: EmailStr


class UpdateUserForm(BaseUser):
    username: str = Form(None)
    email: str = Form(None)
    password: str = Form(None)
