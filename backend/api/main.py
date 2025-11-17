from api.routes import health, pdf, web, agent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from core.config import get_settings
from core.logging import setup_logging
import logging

# Create app
app = FastAPI(
    title="OmniKnow API",
    description="RAG-powered AI agent",
    version="2.0.0"
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()  # Setup
    setup_logging(settings.log_level, settings.log_file)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting OmniKnow API [Environment: {settings.environment}, Vector Store: {settings.vector_store_type}]")

@app.on_event("shutdown")
async def shutdown_event():
    logger = logging.getLogger(__name__)
    logger.info("Shutting down OmniKnow API")

# CORS configuration
settings = get_settings()

# Parse CORS origins (handle both list and JSON string from env)
cors_origins = settings.cors_origins
if isinstance(cors_origins, str):
    import json
    try:
        cors_origins = json.loads(cors_origins)
    except json.JSONDecodeError:
        # Fallback: treat as single origin
        cors_origins = [cors_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Include routers
app.include_router(health.router)
app.include_router(pdf.router)
app.include_router(web.router)
app.include_router(agent.router)