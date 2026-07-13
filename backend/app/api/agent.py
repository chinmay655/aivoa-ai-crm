from fastapi import APIRouter, HTTPException, status

from app.agent.graph import AgentNotConfiguredError, run_agent
from app.agent.tools import TOOLS
from app.schemas import AgentChatRequest, AgentChatResponse

router = APIRouter(prefix="/api/agent", tags=["AI Agent"])


@router.get("/tools")
def list_tools():
    return [
        {
            "name": item.name,
            "description": item.description,
        }
        for item in TOOLS
    ]


@router.post("/chat", response_model=AgentChatResponse)
def chat(payload: AgentChatRequest):
    try:
        response, tools_used = run_agent(payload.message)
        return AgentChatResponse(response=response, tools_used=tools_used)
    except AgentNotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"The AI agent could not complete the request: {exc}",
        ) from exc
