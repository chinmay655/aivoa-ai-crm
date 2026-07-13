from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agent, hcps, interactions
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.seed import seed_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_database(db)
    yield


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-first CRM HCP interaction module using FastAPI, LangGraph, Groq, and SQL.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hcps.router)
app.include_router(interactions.router)
app.include_router(agent.router)


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "model": settings.groq_model,
    }
