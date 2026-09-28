# Setup FastAPI application
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logger import logger
from app.middleware import RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("application_startup", message="Starting CivicPulse backend")
    yield
    # Shutdown
    # Graceful shutdown: FastAPI and Uvicorn handle finishing in-flight requests.
    # Here we close pool connections (e.g., DB/Redis).
    logger.info(
        "application_shutdown",
        message="Closing pool connections and shutting down cleanly",
    )
    # TODO: Close DB and Redis pools here


app = FastAPI(title="CivicPulse", lifespan=lifespan)

# Add Request ID Middleware
app.add_middleware(RequestIdMiddleware)

from app.routes.complaints import router as complaints_router
from app.routes.meta import router as meta_router
from app.routes.monitoring import router as monitoring_router
from app.routes.stats import router as stats_router

app.include_router(complaints_router)
app.include_router(monitoring_router)
app.include_router(meta_router)
app.include_router(stats_router)


@app.get("/health")
def health_check():
    """
    Liveness probe: Process is alive. Must NOT touch the database.
    """
    logger.info("health_check_hit")
    return {"status": "ok"}
