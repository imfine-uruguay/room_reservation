from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateBookingRequest:
    user_id: str
    room_code: str
    title: str
    attendees: int
    start_time: datetime
    end_time: datetime


@dataclass
class CancelBookingRequest:
    user_id: str
    booking_id: int


@dataclass
class AvailabilityRequest:
    room_code: str
    start_time: datetime
    end_time: datetime


@dataclass
class BookingView:
    id: int | None
    room_code: str
    user_id: str
    title: str
    attendees: int
    start_time: datetime
    end_time: datetime
