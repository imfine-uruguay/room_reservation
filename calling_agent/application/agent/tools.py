from datetime import UTC, date as date_cls, datetime

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from calling_agent.application.dto import CancelBookingRequest, CreateBookingRequest
from calling_agent.domain.exceptions import BookingDomainError
from calling_agent.infrastructure.container import BookingContainer
from core.logging.logger import setup_logger

logger = setup_logger(__name__)

_DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class CreateBookingArgs(BaseModel):
    room_code: str = Field(description="Room letter, one of A, B, C, D, E")
    title: str = Field(description="Short title describing the meeting purpose")
    attendees: int = Field(description="Number of people attending the meeting")
    start_time: str = Field(description="Booking start time, format 'YYYY-MM-DD HH:MM'")
    end_time: str = Field(description="Booking end time, format 'YYYY-MM-DD HH:MM'")


class CancelBookingArgs(BaseModel):
    booking_id: int = Field(description="Id of the booking to cancel")


class CheckAvailabilityArgs(BaseModel):
    room_code: str = Field(description="Room letter, one of A, B, C, D, E")
    date: str = Field(description="Day to check, format 'YYYY-MM-DD'")


class ListBookingsArgs(BaseModel):
    pass


def build_agent_tools(user_id: str, container: BookingContainer) -> list[StructuredTool]:
    """Builds the LangGraph tools bound to the currently authenticated user."""

    def create_booking(room_code: str, title: str, attendees: int, start_time: str, end_time: str) -> str:
        try:
            request = CreateBookingRequest(
                user_id=user_id,
                room_code=room_code.strip().upper(),
                title=title,
                attendees=attendees,
                start_time=datetime.strptime(start_time, _DATETIME_FORMAT).replace(tzinfo=UTC),
                end_time=datetime.strptime(end_time, _DATETIME_FORMAT).replace(tzinfo=UTC),
            )
            booking = container.create_booking.execute(request)
            return f"Booking confirmed: id={booking.id}, room={booking.room_code}, {start_time} to {end_time}, title='{booking.title}'"
        except ValueError as e:
            return f"Could not parse the date/time, use 'YYYY-MM-DD HH:MM': {e}"
        except BookingDomainError as e:
            return f"Booking rejected: {e}"
        except RuntimeError as e:
            logger.error(f"Unexpected error creating booking: {e}")
            return "Sorry, an unexpected error happened while creating the booking."

    def cancel_booking(booking_id: int) -> str:
        try:
            container.cancel_booking.execute(CancelBookingRequest(user_id=user_id, booking_id=booking_id))
            return f"Booking {booking_id} was cancelled."
        except BookingDomainError as e:
            return f"Could not cancel booking: {e}"
        except RuntimeError as e:
            logger.error(f"Unexpected error cancelling booking: {e}")
            return "Sorry, an unexpected error happened while cancelling the booking."

    def check_availability(room_code: str, date: str) -> str:
        try:
            target_date = date_cls.fromisoformat(date)
            free_slots = container.check_availability.execute(room_code.strip().upper(), target_date)
            if not free_slots:
                return f"Room {room_code} has no free slots on {date}."
            formatted = ", ".join(
                f"{slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}" for slot in free_slots
            )
            return f"Free 30-minute blocks for room {room_code} on {date}: {formatted}"
        except ValueError as e:
            return f"Could not parse the date, use 'YYYY-MM-DD': {e}"
        except BookingDomainError as e:
            return f"Could not check availability: {e}"
        except RuntimeError as e:
            logger.error(f"Unexpected error checking availability: {e}")
            return "Sorry, an unexpected error happened while checking availability."

    def list_my_bookings() -> str:
        try:
            bookings = container.list_bookings.execute(user_id)
            if not bookings:
                return "You have no bookings."
            lines = [
                f"id={b.id} room={b.room_code} {b.start_time.strftime(_DATETIME_FORMAT)} -> "
                f"{b.end_time.strftime('%H:%M')} title='{b.title}' attendees={b.attendees}"
                for b in bookings
            ]
            return "\n".join(lines)
        except RuntimeError as e:
            logger.error(f"Unexpected error listing bookings: {e}")
            return "Sorry, an unexpected error happened while listing your bookings."

    return [
        StructuredTool.from_function(
            func=create_booking,
            name="create_booking",
            description="Create a new meeting room booking for the active user.",
            args_schema=CreateBookingArgs,
        ),
        StructuredTool.from_function(
            func=cancel_booking,
            name="cancel_booking",
            description="Cancel one of the active user's own bookings by id.",
            args_schema=CancelBookingArgs,
        ),
        StructuredTool.from_function(
            func=check_availability,
            name="check_availability",
            description="List the free 30-minute blocks for a room on a given day.",
            args_schema=CheckAvailabilityArgs,
        ),
        StructuredTool.from_function(
            func=list_my_bookings,
            name="list_my_bookings",
            description="List every booking that belongs to the active user.",
            args_schema=ListBookingsArgs,
        ),
    ]
