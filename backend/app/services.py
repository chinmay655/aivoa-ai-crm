from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session, selectinload

from app import models, schemas


def interaction_query() -> Select[tuple[models.Interaction]]:
    return select(models.Interaction).options(
        selectinload(models.Interaction.hcp),
        selectinload(models.Interaction.samples),
        selectinload(models.Interaction.follow_ups),
    )


def search_hcps(db: Session, query: str = "", limit: int = 20) -> list[models.HCP]:
    statement = select(models.HCP).order_by(models.HCP.name).limit(limit)
    if query.strip():
        pattern = f"%{query.strip()}%"
        statement = (
            select(models.HCP)
            .where(
                or_(
                    models.HCP.name.ilike(pattern),
                    models.HCP.specialty.ilike(pattern),
                    models.HCP.organization.ilike(pattern),
                    models.HCP.city.ilike(pattern),
                )
            )
            .order_by(models.HCP.name)
            .limit(limit)
        )
    return list(db.scalars(statement).all())


def find_hcp_by_name(db: Session, name: str) -> models.HCP | None:
    exact = db.scalar(select(models.HCP).where(models.HCP.name.ilike(name.strip())))
    if exact:
        return exact
    return db.scalar(
        select(models.HCP)
        .where(models.HCP.name.ilike(f"%{name.strip()}%"))
        .order_by(models.HCP.name)
    )


def get_interaction(db: Session, interaction_id: int) -> models.Interaction:
    interaction = db.scalar(interaction_query().where(models.Interaction.id == interaction_id))
    if interaction is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


def list_interactions(
    db: Session, hcp_id: int | None = None, limit: int = 50
) -> list[models.Interaction]:
    statement = interaction_query().order_by(models.Interaction.occurred_at.desc()).limit(limit)
    if hcp_id is not None:
        statement = statement.where(models.Interaction.hcp_id == hcp_id)
    return list(db.scalars(statement).unique().all())


def create_interaction(db: Session, payload: schemas.InteractionCreate) -> models.Interaction:
    hcp = db.get(models.HCP, payload.hcp_id)
    if hcp is None:
        raise HTTPException(status_code=404, detail="HCP not found")

    interaction = models.Interaction(**payload.model_dump())
    db.add(interaction)
    db.commit()
    return get_interaction(db, interaction.id)


def update_interaction(
    db: Session, interaction_id: int, payload: schemas.InteractionUpdate
) -> models.Interaction:
    interaction = get_interaction(db, interaction_id)
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields were provided for update")

    for field, value in changes.items():
        setattr(interaction, field, value)
    db.add(interaction)
    db.commit()
    return get_interaction(db, interaction.id)


def add_sample(
    db: Session,
    interaction_id: int,
    product_name: str,
    quantity: int,
    lot_number: str | None = None,
) -> models.SampleDistribution:
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Sample quantity must be positive")
    get_interaction(db, interaction_id)
    sample = models.SampleDistribution(
        interaction_id=interaction_id,
        product_name=product_name.strip(),
        quantity=quantity,
        lot_number=lot_number.strip() if lot_number else None,
    )
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample


def add_follow_up(
    db: Session, interaction_id: int, due_at: datetime, action: str
) -> models.FollowUp:
    get_interaction(db, interaction_id)
    follow_up = models.FollowUp(
        interaction_id=interaction_id,
        due_at=due_at,
        action=action.strip(),
        status="open",
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)
    return follow_up
