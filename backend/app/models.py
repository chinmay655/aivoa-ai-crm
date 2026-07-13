from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HCP(Base):
    __tablename__ = "hcps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    specialty: Mapped[str] = mapped_column(String(120), index=True)
    organization: Mapped[str] = mapped_column(String(180))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(40))
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)

    interactions: Mapped[list[Interaction]] = relationship(
        back_populates="hcp", cascade="all, delete-orphan"
    )


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    hcp_id: Mapped[int] = mapped_column(ForeignKey("hcps.id"), index=True)
    interaction_type: Mapped[str] = mapped_column(String(60))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    attendees: Mapped[list[str]] = mapped_column(JSON, default=list)
    topics_discussed: Mapped[str] = mapped_column(Text, default="")
    summary: Mapped[str] = mapped_column(Text, default="")
    materials_shared: Mapped[list[str]] = mapped_column(JSON, default=list)
    sentiment: Mapped[str] = mapped_column(String(20), default="neutral")
    outcomes: Mapped[str] = mapped_column(Text, default="")
    next_steps: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="completed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    hcp: Mapped[HCP] = relationship(back_populates="interactions")
    samples: Mapped[list[SampleDistribution]] = relationship(
        back_populates="interaction", cascade="all, delete-orphan"
    )
    follow_ups: Mapped[list[FollowUp]] = relationship(
        back_populates="interaction", cascade="all, delete-orphan"
    )


class SampleDistribution(Base):
    __tablename__ = "sample_distributions"

    id: Mapped[int] = mapped_column(primary_key=True)
    interaction_id: Mapped[int] = mapped_column(ForeignKey("interactions.id"), index=True)
    product_name: Mapped[str] = mapped_column(String(160))
    quantity: Mapped[int] = mapped_column(Integer)
    lot_number: Mapped[str | None] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    interaction: Mapped[Interaction] = relationship(back_populates="samples")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id: Mapped[int] = mapped_column(primary_key=True)
    interaction_id: Mapped[int] = mapped_column(ForeignKey("interactions.id"), index=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    action: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    interaction: Mapped[Interaction] = relationship(back_populates="follow_ups")
