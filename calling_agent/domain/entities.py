from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Room:
    """A meeting room with a fixed seating capacity."""

    code: str
    capacity: int


@dataclass
class Booking:
    """A meeting room reservation owned by a single authenticated user."""

    id: int | None
    room_code: str
    user_id: str
    title: str
    attendees: int
    start_time: datetime
    end_time: datetime
