from fastapi import APIRouter, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os


base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates_dir = os.path.join(base_dir, "templates")
router = APIRouter()
templates = Jinja2Templates(directory=templates_dir)





@router.get("/main", status_code=status.HTTP_200_OK)
async def get_main_page(request: Request):
    return templates.TemplateResponse(
        "/main/main.html",
        {"request": request},
    )
