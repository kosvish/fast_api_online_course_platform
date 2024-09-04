from .main import router as main_router
from fastapi import APIRouter


router = APIRouter()

router.include_router(main_router)
