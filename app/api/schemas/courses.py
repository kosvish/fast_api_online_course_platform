from pydantic import BaseModel, ConfigDict
from .users import ResponseUser


class CourseBase(BaseModel):
    title: str
    description: str | None = None
    code_language: str
    creator_id: int


class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseCreate):
    pass


class CourseUpdatePartial(BaseModel):
    title: str | None = None
    description: str | None = None
    code_language: str | None = None
    # creator_id: int | None = None


class CourseResponse(BaseModel):
    title: str
    description: str | None = None
    code_language: str
    creator: ResponseUser
    price: int


class CourseCreateProd(BaseModel):
    title: str
    description: str | None = None
    code_language: str
