from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HCPRead(BaseModel):
    id: int
    name: str
    specialty: str
    organization: str
    city: str
    state: str
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SampleRead(BaseModel):
    id: int
    product_name: str
    quantity: int
    lot_number: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FollowUpRead(BaseModel):
    id: int
    due_at: datetime
    action: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class InteractionCreate(BaseModel):
    hcp_id: int
    interaction_type: str = Field(min_length=1, max_length=60)
    occurred_at: datetime
    attendees: list[str] = Field(default_factory=list)
    topics_discussed: str = ""
    summary: str = ""
    materials_shared: list[str] = Field(default_factory=list)
    sentiment: str = "neutral"
    outcomes: str = ""
    next_steps: str = ""
    status: str = "completed"

    @field_validator("sentiment")
    @classmethod
    def normalize_sentiment(cls, value: str) -> str:
        normalized = value.strip().lower()
        allowed = {"positive", "neutral", "negative"}
        if normalized not in allowed:
            raise ValueError(f"Sentiment must be one of: {', '.join(sorted(allowed))}")
        return normalized


class InteractionUpdate(BaseModel):
    interaction_type: str | None = None
    occurred_at: datetime | None = None
    attendees: list[str] | None = None
    topics_discussed: str | None = None
    summary: str | None = None
    materials_shared: list[str] | None = None
    sentiment: str | None = None
    outcomes: str | None = None
    next_steps: str | None = None
    status: str | None = None

    @field_validator("sentiment")
    @classmethod
    def normalize_optional_sentiment(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower()
        allowed = {"positive", "neutral", "negative"}
        if normalized not in allowed:
            raise ValueError(f"Sentiment must be one of: {', '.join(sorted(allowed))}")
        return normalized


class InteractionRead(BaseModel):
    id: int
    hcp_id: int
    hcp: HCPRead
    interaction_type: str
    occurred_at: datetime
    attendees: list[str]
    topics_discussed: str
    summary: str
    materials_shared: list[str]
    sentiment: str
    outcomes: str
    next_steps: str
    status: str
    created_at: datetime
    updated_at: datetime
    samples: list[SampleRead] = Field(default_factory=list)
    follow_ups: list[FollowUpRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class AgentChatResponse(BaseModel):
    response: str
    tools_used: list[str] = Field(default_factory=list)
