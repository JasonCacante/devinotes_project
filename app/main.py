from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth_router, label_router, notes_router, share_router
from app.core.config import Settings
from app.core.db import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=Settings.PROJECT_NAME,
    lifespan=lifespan,
    swagger_ui_init_oauth={"persistAuthorization": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(label_router, prefix="/api/v1")
app.include_router(notes_router, prefix="/api/v1")
app.include_router(share_router, prefix="/api/v1")
