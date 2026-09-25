from fastapi import APIRouter, Depends, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Complaint
from app.redis_client import get_stats_cache, set_stats_cache

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


@router.get("")
def get_stats(response: Response, db: Session = Depends(get_db)):
    cached_stats, cache_status = get_stats_cache()
    response.headers["X-Cache"] = cache_status

    if cached_stats:
        return cached_stats

    total = db.query(Complaint).count()

    by_category = (
        db.query(Complaint.category, func.count(Complaint.id))
        .group_by(Complaint.category)
        .all()
    )
    by_priority = (
        db.query(Complaint.priority, func.count(Complaint.id))
        .group_by(Complaint.priority)
        .all()
    )

    stats = {
        "total": total,
        "by_category": {cat.value: count for cat, count in by_category},
        "by_priority": {pri.value: count for pri, count in by_priority},
    }

    set_stats_cache(stats)
    return stats
