from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import signal
import sys
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
    logger.info("application_shutdown", message="Closing pool connections and shutting down cleanly")
    # TODO: Close DB and Redis pools here

app = FastAPI(
    title="CivicPulse",
    lifespan=lifespan
)

# Add Request ID Middleware
app.add_middleware(RequestIdMiddleware)

@app.get("/health")
def health_check():
    """
    Liveness probe: Process is alive. Must NOT touch the database.
    """
    logger.info("health_check_hit")
    return {"status": "ok"}
