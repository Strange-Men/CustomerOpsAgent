"""FastAPI application entry point."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agent import router as agent_router
from app.api.routes_health import router as health_router

app = FastAPI(
    title="CustomerOps Agent",
    description="Cross-border e-commerce customer service RAG Agent demo API",
    version="0.1.0",
)

# CORS: allow frontend origins (Vercel + local dev)
# CUSTOMEROPS_ALLOWED_ORIGINS env var can override (comma-separated)
_default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://customer-ops-agent.vercel.app",
]
_allowed_origins_env = os.environ.get("CUSTOMEROPS_ALLOWED_ORIGINS", "").strip()
allowed_origins = (
    [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]
    if _allowed_origins_env
    else _default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(health_router)
app.include_router(agent_router)
