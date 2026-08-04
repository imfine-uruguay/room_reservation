from auth.domain.entities import User
from auth.domain.exceptions import InvalidCredentialsError
from auth.domain.repositories import AuthRepository
from core.logging.logger import setup_logger

logger = setup_logger(__name__)


class AuthService:
    """Application service used to log in one of the two demo users."""

    def __init__(self, auth_repo: AuthRepository):
        self._auth_repo = auth_repo

    def login(self, username: str, password: str) -> User:
        user = self._auth_repo.verify(username, password)
        if user is None:
            logger.info(f"Failed login attempt for username={username!r}")
            raise InvalidCredentialsError("Invalid username or password")
        logger.info(f"User logged in: {user.user_id}")
        return user
