class BookingDomainError(Exception):
    """Base class for meeting-room booking business rule violations."""


class InvalidTimeSlotError(BookingDomainError):
    """The requested time range is not valid (bad order or not block-aligned)."""


class DurationExceededError(BookingDomainError):
    """The requested booking is longer than the allowed maximum duration."""


class OverlapError(BookingDomainError):
    """The requested slot collides with an existing booking in the room."""


class CapacityExceededError(BookingDomainError):
    """The attendee count is invalid or exceeds the room capacity."""


class RoomNotFoundError(BookingDomainError):
    """The requested room code does not exist."""


class BookingNotFoundError(BookingDomainError):
    """The requested booking id does not exist."""


class NotOwnerError(BookingDomainError):
    """The active user is not the owner of the booking being cancelled."""


class OutsideBusinessHoursError(BookingDomainError):
    """The requested slot falls outside the configured business hours."""
