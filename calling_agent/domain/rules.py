from datetime import time

from calling_agent.domain.entities import Room
from calling_agent.domain.exceptions import (
    CapacityExceededError,
    DurationExceededError,
    InvalidTimeSlotError,
    OutsideBusinessHoursError,
    OverlapError,
)
from calling_agent.domain.repositories import BookingRepository
from calling_agent.domain.value_objects import TimeSlot


class BookingRules:
    """Encapsulates every business rule that a booking must satisfy."""

    def __init__(
        self,
        slot_minutes: int,
        max_duration_minutes: int,
        business_start: time,
        business_end: time,
    ):
        self._slot_minutes = slot_minutes
        self._max_duration_minutes = max_duration_minutes
        self._business_start = business_start
        self._business_end = business_end

    def validate_slot(self, slot: TimeSlot) -> None:
        if slot.end <= slot.start:
            raise InvalidTimeSlotError("End time must be after start time")

        if not slot.is_block_aligned(self._slot_minutes):
            raise InvalidTimeSlotError(f"Booking times must align to {self._slot_minutes}-minute blocks")

        if slot.duration_minutes() > self._max_duration_minutes:
            raise DurationExceededError(f"A booking cannot exceed {self._max_duration_minutes} minutes")

        if slot.start.time() < self._business_start or slot.end.time() > self._business_end:
            raise OutsideBusinessHoursError(
                f"Bookings must fall within business hours ({self._business_start}-{self._business_end})"
            )

    def validate_capacity(self, room: Room, attendees: int) -> None:
        if attendees <= 0:
            raise CapacityExceededError("Attendee count must be a positive number")
        if attendees > room.capacity:
            raise CapacityExceededError(f"Room {room.code} has capacity {room.capacity}, requested {attendees}")

    def validate_no_overlap(
        self,
        room_code: str,
        slot: TimeSlot,
        repo: BookingRepository,
        exclude_booking_id: int | None = None,
    ) -> None:
        existing = repo.list_for_room_between(room_code, slot.start, slot.end)
        for booking in existing:
            if exclude_booking_id is not None and booking.id == exclude_booking_id:
                continue
            other = TimeSlot(booking.start_time, booking.end_time)
            if slot.overlaps(other):
                raise OverlapError(
                    f"Room {room_code} is already booked from {booking.start_time} to {booking.end_time}"
                )
