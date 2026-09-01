import hmac

from auth.domain.entities import User
from auth.domain.repositories import AuthRepository
from core.config.config_manager import ConfigManager


class StaticAuthRepository(AuthRepository):
    """Verifies credentials against the fixed users declared in config.yaml.
    """

    def verify(self, username: str, password: str) -> User | None:
        users: dict = ConfigManager.get("auth.users", {}) or {}
        normalized_username = (username or "").strip()
        record = None
        user_id = None

        if normalized_username:
            for candidate_id, candidate_record in users.items():
                if candidate_id == normalized_username:
                    record = candidate_record
                    user_id = candidate_id
                    break

                if str(candidate_record.get("display_name", "")).strip().lower() == normalized_username.lower():
                    record = candidate_record
                    user_id = candidate_id
                    break

        if record is None:
            return None

        expected_password = str(record.get("password", ""))
        if not hmac.compare_digest(expected_password, password):
            return None

        return User(user_id=user_id or normalized_username, display_name=record.get("display_name", user_id or normalized_username))
