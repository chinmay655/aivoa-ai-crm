from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import HCP


SEED_HCPS = [
    {
        "name": "Dr. Sarah Mitchell",
        "specialty": "Cardiology",
        "organization": "Riverside Heart Center",
        "city": "Newark",
        "state": "NJ",
        "email": "sarah.mitchell@example.test",
    },
    {
        "name": "Dr. Michael Chen",
        "specialty": "Endocrinology",
        "organization": "Metro Endocrine Associates",
        "city": "Jersey City",
        "state": "NJ",
        "email": "michael.chen@example.test",
    },
    {
        "name": "Dr. Priya Patel",
        "specialty": "Oncology",
        "organization": "Garden State Cancer Institute",
        "city": "New Brunswick",
        "state": "NJ",
        "email": "priya.patel@example.test",
    },
    {
        "name": "Dr. James Wilson",
        "specialty": "Internal Medicine",
        "organization": "Harrison Medical Group",
        "city": "Harrison",
        "state": "NJ",
        "email": "james.wilson@example.test",
    },
    {
        "name": "Dr. Emily Rodriguez",
        "specialty": "Neurology",
        "organization": "Hudson Neuroscience Clinic",
        "city": "Hoboken",
        "state": "NJ",
        "email": "emily.rodriguez@example.test",
    },
]


def seed_database(db: Session) -> None:
    count = db.scalar(select(func.count()).select_from(HCP)) or 0
    if count:
        return
    db.add_all([HCP(**item) for item in SEED_HCPS])
    db.commit()
