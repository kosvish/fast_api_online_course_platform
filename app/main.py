from fastapi import FastAPI
from app.db import session
from app.db.models import base
from contextlib import asynccontextmanager
import uvicorn
from app.api.routes import course_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with session.async_engine.begin() as con:
        await con.run_sync(base.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(course_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
