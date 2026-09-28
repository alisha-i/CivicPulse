# Complaints routing logic
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.models import CategoryEnum, PriorityEnum, StatusEnum
from app.redis_client import check_rate_limit, invalidate_stats_cache
from app.repositories import complaint_repo
from app.schemas import ComplaintCreate, ComplaintListResponse, ComplaintResponse
from app.services import triage_service

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])


@router.post("", response_model=ComplaintResponse, status_code=201)
def submit_complaint(
    request: Request, complaint: ComplaintCreate, db: Session = Depends(get_db)
):
    logger.info("submit_complaint_started")

    # Rate Limiting
    client_ip = request.client.host if request.client else "127.0.0.1"
    allowed, retry_after = check_rate_limit(client_ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)},
        )

    triage_result = triage_service.perform_triage(complaint)
    db_complaint = complaint_repo.create_complaint(db, complaint, triage_result)

    invalidate_stats_cache()

    logger.info("submit_complaint_success", complaint_id=str(db_complaint.id))
    return db_complaint


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: UUID, db: Session = Depends(get_db)):
    db_complaint = complaint_repo.get_complaint(db, complaint_id)
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint


@router.get("", response_model=ComplaintListResponse)
def list_complaints(
    category: CategoryEnum | None = None,
    priority: PriorityEnum | None = None,
    status: StatusEnum | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total, items = complaint_repo.list_complaints(
        db, category, priority, status, page, page_size
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


from app.schemas import ComplaintStatusUpdate

VALID_TRANSITIONS = {
    StatusEnum.open: {StatusEnum.in_progress, StatusEnum.rejected},
    StatusEnum.in_progress: {StatusEnum.resolved, StatusEnum.rejected},
    StatusEnum.resolved: set(),
    StatusEnum.rejected: set(),
}


@router.patch("/{complaint_id}/status", response_model=ComplaintResponse)
def update_complaint_status(
    complaint_id: UUID,
    status_update: ComplaintStatusUpdate,
    db: Session = Depends(get_db),
):
    db_complaint = complaint_repo.get_complaint(db, complaint_id)
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    current_status = db_complaint.status
    new_status = status_update.status

    if new_status not in VALID_TRANSITIONS[current_status]:
        raise HTTPException(
            status_code=409,
            detail=f"Invalid transition from {current_status.value} to {new_status.value}",
        )

    db_complaint.status = new_status
    db.commit()
    db.refresh(db_complaint)

    invalidate_stats_cache()

    logger.info(
        "complaint_status_updated",
        complaint_id=str(complaint_id),
        old=current_status.value,
        new=new_status.value,
    )
    return db_complaint
