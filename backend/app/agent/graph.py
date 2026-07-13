from functools import lru_cache
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, MessagesState, StateGraph

from app.agent.tools import TOOLS, TOOLS_BY_NAME
from app.config import get_settings


SYSTEM_PROMPT = """
You are the AI assistant inside a life-sciences CRM used by field representatives.
Your job is to accurately manage Healthcare Professional interactions.

Rules:
- Use a tool whenever the user asks to search, create, edit, add a sample, schedule a follow-up, or retrieve history.
- Never invent an HCP, interaction ID, product sample, or database result.
- Ask one concise clarification question when required information is missing.
- For logging, extract a concise factual summary, entities, materials, sentiment, outcomes, and next steps from the user's notes.
- Sentiment must be positive, neutral, or negative.
- Use ISO-8601 dates and times in tool arguments. When the user's date is ambiguous, ask for clarification.
- After a successful tool call, confirm the action and include the created or updated record ID.
- Do not include sensitive patient information. Ask the user to remove patient-identifying data if supplied.
""".strip()


class AgentNotConfiguredError(RuntimeError):
    pass


@lru_cache
def build_agent():
    settings = get_settings()
    if not settings.groq_api_key:
        raise AgentNotConfiguredError(
            "GROQ_API_KEY is not configured. Add it to backend/.env or the root .env file."
        )

    model = ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0,
        max_retries=2,
    )
    model_with_tools = model.bind_tools(TOOLS)

    def assistant_node(state: MessagesState):
        response = model_with_tools.invoke(
            [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
        )
        return {"messages": [response]}

    def tool_node(state: MessagesState):
        results: list[ToolMessage] = []
        last_message = state["messages"][-1]
        for tool_call in last_message.tool_calls:
            selected_tool = TOOLS_BY_NAME[tool_call["name"]]
            observation = selected_tool.invoke(tool_call["args"])
            results.append(
                ToolMessage(
                    content=str(observation),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                )
            )
        return {"messages": results}

    def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
        last_message = state["messages"][-1]
        return "tools" if getattr(last_message, "tool_calls", None) else END

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", should_continue, ["tools", END])
    builder.add_edge("tools", "assistant")
    return builder.compile()


def run_agent(message: str) -> tuple[str, list[str]]:
    agent = build_agent()
    result = agent.invoke({"messages": [HumanMessage(content=message)]})

    tools_used: list[str] = []
    for item in result["messages"]:
        for call in getattr(item, "tool_calls", []) or []:
            name = call.get("name")
            if name and name not in tools_used:
                tools_used.append(name)

    final_message = result["messages"][-1]
    content = final_message.content
    if isinstance(content, list):
        content = " ".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        ).strip()
    return str(content), tools_used
