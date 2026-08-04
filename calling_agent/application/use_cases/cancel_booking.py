from calling_agent.application.dto import CancelBookingRequest
from calling_agent.domain.exceptions import BookingNotFoundError, NotOwnerError
from calling_agent.domain.repositories import BookingRepository
from core.logging.logger import setup_logger

logger = setup_logger(__name__)


class CancelBookingUseCase:
    """Cancels a booking, only if it belongs to the requesting user."""

    def __init__(self, booking_repo: BookingRepository):
        self._booking_repo = booking_repo

    def execute(self, request: CancelBookingRequest) -> None:
        booking = self._booking_repo.get_by_id(request.booking_id)
        if booking is None:
            raise BookingNotFoundError(f"Booking {request.booking_id} does not exist")

        if booking.user_id != request.user_id:
            raise NotOwnerError("You can only cancel your own bookings")

        self._booking_repo.delete(request.booking_id)
        logger.info(f"Booking cancelled: id={request.booking_id} user={request.user_id}")
