import os
import sys
import uuid

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.database import SessionLocal
from app.models import CategoryEnum, Complaint, PriorityEnum, StatusEnum

COMPLAINT_TEMPLATES = [
    (
        "bhai street {n} mein paani bhar gaya hai fajr se",
        CategoryEnum.water,
        PriorityEnum.high,
    ),
    (
        "meri gali {n} ki light pichlay 2 din se kharab hai",
        CategoryEnum.streetlights,
        PriorityEnum.normal,
    ),
    (
        "sector {n} ki sarak bilkul toot gayi hai, gari phas jati hai",
        CategoryEnum.roads,
        PriorityEnum.high,
    ),
    (
        "gali {n} mein kachra uthane wala nahi aya pura hafta",
        CategoryEnum.sanitation,
        PriorityEnum.low,
    ),
    (
        "bijli ka transformer blast ho gaya hai block {n} mein",
        CategoryEnum.electricity,
        PriorityEnum.high,
    ),
    (
        "paani ki line leak kar rahi hai house {n} k bahar",
        CategoryEnum.water,
        PriorityEnum.normal,
    ),
    (
        "kal se light nahi hai area {n} mein",
        CategoryEnum.electricity,
        PriorityEnum.high,
    ),
    (
        "gutter overflow kar raha hai phase {n} market k pas",
        CategoryEnum.sanitation,
        PriorityEnum.high,
    ),
    (
        "street {n} par road repair ka kaam incomplete chhor diya",
        CategoryEnum.roads,
        PriorityEnum.low,
    ),
    (
        "streetlight pole {n} girne wala hai",
        CategoryEnum.streetlights,
        PriorityEnum.high,
    ),
]


def generate_seed_data():
    seed_data = []
    # Generate 30 fixed but realistic complaints
    for i in range(1, 31):
        template, category, priority = COMPLAINT_TEMPLATES[i % len(COMPLAINT_TEMPLATES)]

        # We use a deterministic UUID based on the loop index so that it's truly idempotent
        deterministic_id = uuid.uuid5(uuid.NAMESPACE_OID, f"complaint-{i}")

        seed_data.append(
            {
                "id": deterministic_id,
                "text": template.format(n=i),
                "location": f"Area {i}, City",
                "category": category,
                "priority": priority,
                "status": StatusEnum.open,
                "ai_summary": "Auto generated seed data",
                "triaged_by": "simulated",
                "triage_latency_ms": 150,
            }
        )
    return seed_data


def run_seed():
    db = SessionLocal()
    try:
        data = generate_seed_data()
        for item in data:
            stmt = pg_insert(Complaint).values(**item)
            # Idempotency: Do nothing if the complaint ID already exists
            stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
            db.execute(stmt)
        db.commit()
        print(f"Successfully seeded {len(data)} complaints. (Idempotent run)")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
