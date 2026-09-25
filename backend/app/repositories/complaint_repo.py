from uuid import UUID

from sqlalchemy.orm import Session

from app.models import CategoryEnum, Complaint, PriorityEnum, StatusEnum
from app.schemas import ComplaintCreate


def create_complaint(
    db: Session, complaint: ComplaintCreate, triage_result: dict
) -> Complaint:
    db_complaint = Complaint(
        text=complaint.text,
        location=complaint.location,
        reporter_contact=complaint.reporter_contact,
        category=triage_result["category"],
        priority=triage_result["priority"],
        ai_summary=triage_result.get("summary"),
        triaged_by=triage_result.get("triaged_by"),
        triage_latency_ms=triage_result.get("triage_latency_ms"),
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def get_complaint(db: Session, complaint_id: UUID) -> Complaint | None:
    return db.query(Complaint).filter(Complaint.id == complaint_id).first()


def list_complaints(
    db: Session,
    category: CategoryEnum | None = None,
    priority: PriorityEnum | None = None,
    status: StatusEnum | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[int, list[Complaint]]:
    query = db.query(Complaint)
    if category:
        query = query.filter(Complaint.category == category)
    if priority:
        query = query.filter(Complaint.priority == priority)
    if status:
        query = query.filter(Complaint.status == status)

    total = query.count()
    items = (
        query.order_by(Complaint.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, items
