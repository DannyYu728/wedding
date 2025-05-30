from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import NotFoundError, DuplicateError

from app.api.auth           import router as auth_router
from app.api.users          import router as users_router
from app.api.dinner_options import router as dinner_router
from app.api.plus_one       import router as plus_one_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic (e.g. connect to external services) goes here
    yield
    # shutdown logic (e.g. cleanup, closing connections) goes here

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(dinner_router)
app.include_router(plus_one_router)

@app.exception_handler(NotFoundError)
async def handle_not_found(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(DuplicateError)
async def handle_duplicate(request: Request, exc: DuplicateError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

