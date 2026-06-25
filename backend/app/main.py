"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.agent import router as agent_router
from app.api.routes_health import router as health_router

app = FastAPI(
    title="CustomerOps Agent",
    description="Cross-border e-commerce customer service RAG Agent demo API",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(agent_router)
