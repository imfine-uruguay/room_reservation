from langchain_openai import ChatOpenAI

from core.config.config_manager import ConfigManager


def build_chat_model() -> ChatOpenAI:
    """Builds the chat model pointed at the GROP OpenAI compatible endpoint."""
    return ChatOpenAI(
        model=ConfigManager.get_llm_model_name_in_grop(),
        base_url=ConfigManager.get_llm_model_url(),
        api_key=ConfigManager.get_llm_model_api_key(),
        temperature=ConfigManager.get_llm_model_temperature(),
        max_tokens=ConfigManager.get("llm.max_tokens", 2048),
        max_retries=ConfigManager.get("llm.max_retries", 2),
    )
