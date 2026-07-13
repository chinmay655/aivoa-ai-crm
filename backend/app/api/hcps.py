from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas, services
from app.database import get_db

router = APIRouter(prefix="/api/hcps", tags=["HCPs"])


@router.get("", response_model=list[schemas.HCPRead])
def search_hcps(
    q: str = Query(default="", max_length=120),
    db: Session = Depends(get_db),
):
    return services.search_hcps(db, query=q)
