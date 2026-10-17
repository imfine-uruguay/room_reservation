from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta

from calling_agent.domain.exceptions import RoomNotFoundError
from calling_agent.domain.repositories import BookingRepository, RoomRepository
from calling_agent.domain.value_objects import TimeSlot
from core.logging.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class FreeSlot:
    start_time: datetime
    end_time: datetime


class CheckAvailabilityUseCase:
    """Computes the free 30-minute blocks for a room on a given day."""

    def __init__(
        self,
        booking_repo: BookingRepository,
        room_repo: RoomRepository,
        slot_minutes: int,
        business_start: time,
        business_end: time,
    ):
        self._booking_repo = booking_repo
        self._room_repo = room_repo
        self._slot_minutes = slot_minutes
        self._business_start = business_start
        self._business_end = business_end

    def execute(self, room_code: str, target_date: date) -> list[FreeSlot]:
        room = self._room_repo.get_by_code(room_code)
        if room is None:
            raise RoomNotFoundError(f"Room {room_code} does not exist")

        day_start = datetime.combine(target_date, self._business_start, tzinfo=UTC)
        day_end = datetime.combine(target_date, self._business_end, tzinfo=UTC)

        bookings = self._booking_repo.list_for_room_between(room_code, day_start, day_end)
        booked_slots = [TimeSlot(b.start_time, b.end_time) for b in bookings]

        step = timedelta(minutes=self._slot_minutes)
        free_slots: list[FreeSlot] = []
        cursor = day_start
        while cursor + step <= day_end:
            candidate = TimeSlot(cursor, cursor + step)
            if not any(candidate.overlaps(busy) for busy in booked_slots):
                free_slots.append(FreeSlot(candidate.start, candidate.end))
            cursor += step

        return free_slots

    def is_range_free(self, room_code: str, start_time: datetime, end_time: datetime) -> bool:
        room = self._room_repo.get_by_code(room_code)
        if room is None:
            raise RoomNotFoundError(f"Room {room_code} does not exist")

        slot = TimeSlot(start_time, end_time)
        existing = self._booking_repo.list_for_room_between(room_code, start_time, end_time)
        return not any(slot.overlaps(TimeSlot(b.start_time, b.end_time)) for b in existing)
