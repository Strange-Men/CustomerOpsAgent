"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.routes_health import router as health_router

app = FastAPI(
    title="CustomerOps Agent",
    description="售后客服工单多 Agent 工作台 API",
    version="0.1.0",
)

app.include_router(health_router)
