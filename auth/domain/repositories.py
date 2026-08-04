from abc import ABC, abstractmethod

from auth.domain.entities import User


class AuthRepository(ABC):
    """Port for verifying credentials of the two fixed demo users."""

    @abstractmethod
    def verify(self, username: str, password: str) -> User | None: ...
