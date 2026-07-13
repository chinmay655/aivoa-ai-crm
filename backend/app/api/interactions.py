from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import schemas, services
from app.database import get_db

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])


@router.get("", response_model=list[schemas.InteractionRead])
def list_interactions(
    hcp_id: int | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return services.list_interactions(db, hcp_id=hcp_id, limit=limit)


@router.post("", response_model=schemas.InteractionRead, status_code=status.HTTP_201_CREATED)
def create_interaction(
    payload: schemas.InteractionCreate,
    db: Session = Depends(get_db),
):
    return services.create_interaction(db, payload)


@router.patch("/{interaction_id}", response_model=schemas.InteractionRead)
def edit_interaction(
    interaction_id: int,
    payload: schemas.InteractionUpdate,
    db: Session = Depends(get_db),
):
    return services.update_interaction(db, interaction_id, payload)
