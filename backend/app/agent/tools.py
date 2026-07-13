import json
from datetime import datetime, timezone

from langchain_core.tools import tool
from sqlalchemy.exc import SQLAlchemyError

from app import schemas, services
from app.database import SessionLocal


def _parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    cleaned = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(cleaned)
    except ValueError as exc:
        raise ValueError(
            "Use an ISO date/time such as 2026-07-14T14:30:00-04:00"
        ) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _json(data: dict | list) -> str:
    return json.dumps(data, default=str)


@tool

def search_hcp(query: str) -> str:
    """Search HCPs by name, specialty, organization, or city before logging an interaction."""
    with SessionLocal() as db:
        matches = services.search_hcps(db, query=query, limit=10)
        return _json(
            [
                {
                    "id": hcp.id,
                    "name": hcp.name,
                    "specialty": hcp.specialty,
                    "organization": hcp.organization,
                    "location": f"{hcp.city}, {hcp.state}",
                }
                for hcp in matches
            ]
        )


@tool

def log_interaction(
    hcp_name: str,
    interaction_type: str,
    occurred_at: str | None = None,
    attendees: list[str] | None = None,
    topics_discussed: str = "",
    summary: str = "",
    materials_shared: list[str] | None = None,
    sentiment: str = "neutral",
    outcomes: str = "",
    next_steps: str = "",
) -> str:
    """Log a new HCP interaction. Extract structured fields from the user's natural-language notes."""
    with SessionLocal() as db:
        hcp = services.find_hcp_by_name(db, hcp_name)
        if hcp is None:
            return _json(
                {
                    "success": False,
                    "error": "HCP not found. Use search_hcp and ask the user to select a valid HCP.",
                }
            )
        try:
            payload = schemas.InteractionCreate(
                hcp_id=hcp.id,
                interaction_type=interaction_type,
                occurred_at=_parse_datetime(occurred_at),
                attendees=attendees or [],
                topics_discussed=topics_discussed,
                summary=summary,
                materials_shared=materials_shared or [],
                sentiment=sentiment,
                outcomes=outcomes,
                next_steps=next_steps,
            )
            interaction = services.create_interaction(db, payload)
            return _json(
                {
                    "success": True,
                    "interaction_id": interaction.id,
                    "hcp": interaction.hcp.name,
                    "occurred_at": interaction.occurred_at,
                    "summary": interaction.summary,
                    "sentiment": interaction.sentiment,
                }
            )
        except (ValueError, SQLAlchemyError) as exc:
            db.rollback()
            return _json({"success": False, "error": str(exc)})


@tool

def edit_interaction(
    interaction_id: int,
    interaction_type: str | None = None,
    topics_discussed: str | None = None,
    summary: str | None = None,
    sentiment: str | None = None,
    outcomes: str | None = None,
    next_steps: str | None = None,
    status: str | None = None,
) -> str:
    """Edit selected fields of an existing interaction without replacing unspecified fields."""
    with SessionLocal() as db:
        try:
            changes = {
                "interaction_type": interaction_type,
                "topics_discussed": topics_discussed,
                "summary": summary,
                "sentiment": sentiment,
                "outcomes": outcomes,
                "next_steps": next_steps,
                "status": status,
            }
            payload = schemas.InteractionUpdate(
                **{field: value for field, value in changes.items() if value is not None}
            )
            interaction = services.update_interaction(db, interaction_id, payload)
            return _json(
                {
                    "success": True,
                    "interaction_id": interaction.id,
                    "summary": interaction.summary,
                    "sentiment": interaction.sentiment,
                    "next_steps": interaction.next_steps,
                }
            )
        except Exception as exc:  # Tool must return an actionable observation to the agent.
            db.rollback()
            detail = getattr(exc, "detail", str(exc))
            return _json({"success": False, "error": detail})


@tool

def add_product_sample(
    interaction_id: int,
    product_name: str,
    quantity: int,
    lot_number: str | None = None,
) -> str:
    """Add product samples distributed during a specific interaction."""
    with SessionLocal() as db:
        try:
            sample = services.add_sample(
                db,
                interaction_id=interaction_id,
                product_name=product_name,
                quantity=quantity,
                lot_number=lot_number,
            )
            return _json(
                {
                    "success": True,
                    "sample_id": sample.id,
                    "interaction_id": interaction_id,
                    "product_name": sample.product_name,
                    "quantity": sample.quantity,
                    "lot_number": sample.lot_number,
                }
            )
        except Exception as exc:
            db.rollback()
            detail = getattr(exc, "detail", str(exc))
            return _json({"success": False, "error": detail})


@tool

def schedule_follow_up(interaction_id: int, due_at: str, action: str) -> str:
    """Schedule a future sales follow-up associated with an interaction."""
    with SessionLocal() as db:
        try:
            follow_up = services.add_follow_up(
                db,
                interaction_id=interaction_id,
                due_at=_parse_datetime(due_at),
                action=action,
            )
            return _json(
                {
                    "success": True,
                    "follow_up_id": follow_up.id,
                    "interaction_id": interaction_id,
                    "due_at": follow_up.due_at,
                    "action": follow_up.action,
                }
            )
        except Exception as exc:
            db.rollback()
            detail = getattr(exc, "detail", str(exc))
            return _json({"success": False, "error": detail})


@tool

def get_interaction_history(hcp_name: str, limit: int = 5) -> str:
    """Retrieve recent interactions for an HCP to help a representative prepare for a visit."""
    with SessionLocal() as db:
        hcp = services.find_hcp_by_name(db, hcp_name)
        if hcp is None:
            return _json({"success": False, "error": "HCP not found"})
        interactions = services.list_interactions(db, hcp_id=hcp.id, limit=min(limit, 20))
        return _json(
            {
                "success": True,
                "hcp": hcp.name,
                "interactions": [
                    {
                        "id": item.id,
                        "occurred_at": item.occurred_at,
                        "type": item.interaction_type,
                        "summary": item.summary,
                        "sentiment": item.sentiment,
                        "outcomes": item.outcomes,
                        "next_steps": item.next_steps,
                    }
                    for item in interactions
                ],
            }
        )


TOOLS = [
    search_hcp,
    log_interaction,
    edit_interaction,
    add_product_sample,
    schedule_follow_up,
    get_interaction_history,
]
TOOLS_BY_NAME = {item.name: item for item in TOOLS}
