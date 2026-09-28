# Health and monitoring endpoints
import redis
from fastapi import APIRouter, Depends, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(tags=["Monitoring"])

# Prometheus Metrics definition
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP Request Latency", ["method", "endpoint"]
)
TRIAGE_LATENCY = Histogram("triage_duration_seconds", "Triage Latency", ["provider"])
FALLBACK_COUNT = Counter(
    "triage_fallback_total", "Total times AI triage fell back to rules"
)


@router.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness probe: 200 only if Postgres and Redis are reachable;
    503 naming the failed dependency.
    """
    failed_deps = []

    # Check Postgres
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        failed_deps.append("postgres")

    # Check Redis (Defaulting to localhost or environment var in future)
    try:
        r = redis.Redis(host="localhost", port=6379, socket_timeout=1)
        r.ping()
    except Exception:
        failed_deps.append("redis")

    if failed_deps:
        raise HTTPException(
            status_code=503, detail=f"Dependencies failed: {', '.join(failed_deps)}"
        )

    return {"status": "ready"}


@router.get("/metrics")
def metrics():
    """
    Prometheus text format: request count, request latency histogram,
    triage latency, fallback counter.
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# Keep these endpoints light to avoid performance hits
