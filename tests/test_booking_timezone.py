from datetime import UTC, datetime, time

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from calling_agent.application.use_cases.list_bookings import ListBookingsUseCase
from calling_agent.domain.entities import Booking
from calling_agent.domain.exceptions import OverlapError
from calling_agent.domain.rules import BookingRules
from calling_agent.domain.value_objects import TimeSlot
from calling_agent.infrastructure.persistence.sqlalchemy_repositories import (
    SqlAlchemyBookingRepository,
)
from utils.database.models import Base, RoomModel


class InMemoryBookingRepository:
    def __init__(self, bookings: list[Booking]) -> None:
        self._bookings = bookings

    def list_for_user(self, user_id: str) -> list[Booking]:
        return [booking for booking in self._bookings if booking.user_id == user_id]


def test_latest_booking_returns_only_most_recently_created_user_booking() -> None:
    bookings = [
        Booking(
            id=1,
            room_code="A",
            user_id="user-1",
            title="First meeting",
            attendees=2,
            start_time=datetime(2026, 10, 17, 10, 0, tzinfo=UTC),
            end_time=datetime(2026, 10, 17, 11, 0, tzinfo=UTC),
        ),
        Booking(
            id=2,
            room_code="A",
            user_id="user-1",
            title="Latest meeting",
            attendees=3,
            start_time=datetime(2026, 10, 17, 11, 0, tzinfo=UTC),
            end_time=datetime(2026, 10, 17, 12, 0, tzinfo=UTC),
        ),
        Booking(
            id=3,
            room_code="B",
            user_id="user-2",
            title="Another user's meeting",
            attendees=1,
            start_time=datetime(2026, 10, 17, 12, 0, tzinfo=UTC),
            end_time=datetime(2026, 10, 17, 13, 0, tzinfo=UTC),
        ),
    ]
    use_case = ListBookingsUseCase(InMemoryBookingRepository(bookings))

    latest = use_case.execute_latest("user-1")

    assert latest is not None
    assert latest.id == 2
    assert latest.title == "Latest meeting"


def test_latest_booking_returns_none_when_user_has_no_bookings() -> None:
    use_case = ListBookingsUseCase(InMemoryBookingRepository([]))

    assert use_case.execute_latest("user-1") is None


def test_existing_booking_with_sqlite_datetime_blocks_overlapping_booking() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    with session_factory() as session:
        session.add(RoomModel(code="A", capacity=4))
        session.commit()

    booking_repo = SqlAlchemyBookingRepository(session_factory)
    booking_repo.add(
        Booking(
            id=None,
            room_code="A",
            user_id="user-1",
            title="Existing meeting",
            attendees=2,
            start_time=datetime(2026, 10, 17, 10, 0, tzinfo=UTC),
            end_time=datetime(2026, 10, 17, 11, 0, tzinfo=UTC),
        )
    )

    rules = BookingRules(
        slot_minutes=30,
        max_duration_minutes=180,
        business_start=time(8),
        business_end=time(18),
    )
    requested_slot = TimeSlot(
        datetime(2026, 10, 17, 10, 30, tzinfo=UTC),
        datetime(2026, 10, 17, 11, 30, tzinfo=UTC),
    )

    with pytest.raises(OverlapError):
        rules.validate_no_overlap("A", requested_slot, booking_repo)
