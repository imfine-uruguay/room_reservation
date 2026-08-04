from langchain_core.messages import HumanMessage

from auth.application.auth_service import AuthService
from auth.domain.exceptions import InvalidCredentialsError
from auth.infrastructure.static_auth_repository import StaticAuthRepository
from calling_agent.application.agent.graph_builder import build_agent_for_user
from core.logging.logger import setup_logger
from utils.database.init_db import init_db

logger = setup_logger(__name__)


def _login():
    auth_service = AuthService(StaticAuthRepository())
    print("=== Cubo Itau meeting room assistant ===")
    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        try:
            return auth_service.login(username, password)
        except InvalidCredentialsError:
            print("Invalid username or password, try again.\n")


def _chat_loop(agent, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    print("\nYou're connected. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            return
        if not user_input:
            continue

        result = agent.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
        reply = result["messages"][-1].content
        print(f"Assistant: {reply}\n")


def main():
    init_db()
    user = _login()
    agent = build_agent_for_user(user)
    _chat_loop(agent, thread_id=user.user_id)


if __name__ == "__main__":
    main()
