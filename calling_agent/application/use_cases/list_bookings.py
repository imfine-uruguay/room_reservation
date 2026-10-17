from calling_agent.application.dto import BookingView
from calling_agent.domain.repositories import BookingRepository


class ListBookingsUseCase:
    """Lists every booking that belongs to the active user."""

    def __init__(self, booking_repo: BookingRepository):
        self._booking_repo = booking_repo

    def execute(self, user_id: str) -> list[BookingView]:
        bookings = self._booking_repo.list_for_user(user_id)
        return [BookingView(**b.__dict__) for b in bookings]

    def execute_latest(self, user_id: str) -> BookingView | None:
        bookings = self._booking_repo.list_for_user(user_id)
        if not bookings:
            return None
        latest = max(bookings, key=lambda booking: booking.id or 0)
        return BookingView(**latest.__dict__)
