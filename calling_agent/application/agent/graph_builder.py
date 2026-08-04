from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from auth.domain.entities import User
from calling_agent.application.agent.tools import build_agent_tools
from calling_agent.infrastructure.container import BookingContainer
from calling_agent.infrastructure.llm.llm_client import build_chat_model
from core.config.config_manager import ConfigManager


def build_agent_for_user(user: User):
    container = BookingContainer()
    tools = build_agent_tools(user.user_id, container)
    model = build_chat_model()

    base_prompt = ConfigManager.get("call_agent.system_prompt", "")
    system_prompt = f"{base_prompt}\n\nThe active authenticated user is: {user.user_id} ({user.display_name})."

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=MemorySaver(),
    )