from .main import router as main_router
from .course import router as course_router
from fastapi import APIRouter


router = APIRouter(prefix='/pages', tags=['Pages'])

router.include_router(main_router)
router.include_router(course_router, prefix='/courses')
