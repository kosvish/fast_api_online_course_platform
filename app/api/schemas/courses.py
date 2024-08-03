from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    title: str
    description: str | None = None
    code_language: str
    mentor: str


class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseCreate):
    pass


class CourseUpdatePartial(CourseCreate):
    title: str | None = None
    description: str | None = None
    code_language: str | None = None
    mentor: str | None = None

