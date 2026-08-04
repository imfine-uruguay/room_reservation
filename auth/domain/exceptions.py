class AuthDomainError(Exception):
    """Base class for authentication failures."""


class InvalidCredentialsError(AuthDomainError):
    """Raised when the username/password pair does not match a known user."""
