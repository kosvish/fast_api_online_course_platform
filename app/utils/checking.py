from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import CourseModel, UserModel


def check_user_in_course_participants(
    course_with_participants: CourseModel, user: UserModel
):
    if user in course_with_participants.participants:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You already joined at course: {course_with_participants.title}",
        )
    return True


def check_is_owner_user_course(course: CourseModel, user: UserModel):
    if course.creator_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You cannot edit, this course'
        )
    return True
