from calling_agent.application.dto import BookingView, CreateBookingRequest
from calling_agent.domain.entities import Booking
from calling_agent.domain.exceptions import RoomNotFoundError
from calling_agent.domain.repositories import BookingRepository, RoomRepository
from calling_agent.domain.rules import BookingRules
from calling_agent.domain.value_objects import TimeSlot
from core.logging.logger import setup_logger

logger = setup_logger(__name__)


class CreateBookingUseCase:
    """Creates a new booking after validating every business rule."""

    def __init__(self, booking_repo: BookingRepository, room_repo: RoomRepository, rules: BookingRules):
        self._booking_repo = booking_repo
        self._room_repo = room_repo
        self._rules = rules

    def execute(self, request: CreateBookingRequest) -> BookingView:
        room = self._room_repo.get_by_code(request.room_code)
        if room is None:
            raise RoomNotFoundError(f"Room {request.room_code} does not exist")

        slot = TimeSlot(request.start_time, request.end_time)
        self._rules.validate_slot(slot)
        self._rules.validate_capacity(room, request.attendees)
        self._rules.validate_no_overlap(room.code, slot, self._booking_repo)

        booking = Booking(
            id=None,
            room_code=room.code,
            user_id=request.user_id,
            title=request.title,
            attendees=request.attendees,
            start_time=request.start_time,
            end_time=request.end_time,
        )
        saved = self._booking_repo.add(booking)
        logger.info(f"Booking created: room={saved.room_code} user={saved.user_id} id={saved.id}")
        return BookingView(**saved.__dict__)
