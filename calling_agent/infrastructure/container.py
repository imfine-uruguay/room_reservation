from datetime import time

from calling_agent.application.use_cases.cancel_booking import CancelBookingUseCase
from calling_agent.application.use_cases.check_availability import (
    CheckAvailabilityUseCase,
)
from calling_agent.application.use_cases.create_booking import CreateBookingUseCase
from calling_agent.application.use_cases.list_bookings import ListBookingsUseCase
from calling_agent.domain.rules import BookingRules
from calling_agent.infrastructure.persistence.sqlalchemy_repositories import (
    SqlAlchemyBookingRepository,
    SqlAlchemyRoomRepository,
)
from core.config.config_manager import ConfigManager
from utils.database.session import SessionLocal


def _parse_time(value: str) -> time:
    hour, minute = value.split(":")
    return time(int(hour), int(minute))


class BookingContainer:
    """Dependency injection container wiring the booking vertical slice."""

    def __init__(self):
        self.booking_repo = SqlAlchemyBookingRepository(SessionLocal)
        self.room_repo = SqlAlchemyRoomRepository(SessionLocal)

        slot_minutes = ConfigManager.get("call_agent.slot_minutes", 30)
        max_duration = ConfigManager.get("call_agent.max_duration_minutes", 180)
        business_hours = ConfigManager.get("call_agent.business_hours", {}) or {}
        business_start = _parse_time(business_hours.get("start", "08:00"))
        business_end = _parse_time(business_hours.get("end", "20:00"))

        self.rules = BookingRules(
            slot_minutes=slot_minutes,
            max_duration_minutes=max_duration,
            business_start=business_start,
            business_end=business_end,
        )

        self.create_booking = CreateBookingUseCase(self.booking_repo, self.room_repo, self.rules)
        self.cancel_booking = CancelBookingUseCase(self.booking_repo)
        self.check_availability = CheckAvailabilityUseCase(
            self.booking_repo, self.room_repo, slot_minutes, business_start, business_end
        )
        self.list_bookings = ListBookingsUseCase(self.booking_repo)
