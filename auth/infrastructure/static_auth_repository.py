import hmac

from auth.domain.entities import User
from auth.domain.repositories import AuthRepository
from core.config.config_manager import ConfigManager


class StaticAuthRepository(AuthRepository):
    """Verifies credentials against the fixed users declared in config.yaml.
    """

    def verify(self, username: str, password: str) -> User | None:
        users: dict = ConfigManager.get("auth.users", {}) or {}
        record = users.get(username)
        if record is None:
            return None

        expected_password = str(record.get("password", ""))
        if not hmac.compare_digest(expected_password, password):
            return None

        return User(user_id=username, display_name=record.get("display_name", username))
