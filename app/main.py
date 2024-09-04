from fastapi import FastAPI
from app.db import session
from app.db.models import base
from contextlib import asynccontextmanager
import uvicorn
from app.api.routes import course_router, user_router
from app.api.demo_auth.views import router as demo_auth_router

# from app.api.demo_auth.demo_jwt_auth import router as demo_auth_jwt_router
from app.api.auth import auth_router
from fastapi.staticfiles import StaticFiles
from app.pages_routes import router as pages_router
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with session.async_engine.begin() as con:
        await con.run_sync(base.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(course_router)
app.include_router(user_router)
# app.include_router(demo_auth_router)
# app.include_router(demo_auth_jwt_router)
app.include_router(auth_router)
app.include_router(pages_router)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(base_dir, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
