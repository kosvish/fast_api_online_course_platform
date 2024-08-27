from fastapi import FastAPI
from app.db import session
from app.db.models import base
from contextlib import asynccontextmanager
import uvicorn
from app.api.routes import course_router, user_router
from app.api.demo_auth.views import router as demo_auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with session.async_engine.begin() as con:
        await con.run_sync(base.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(course_router)
app.include_router(user_router)
app.include_router(demo_auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
