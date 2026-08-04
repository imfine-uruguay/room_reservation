from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """An authenticated user allowed to manage their own bookings."""
    user_id: str
    display_name: str
