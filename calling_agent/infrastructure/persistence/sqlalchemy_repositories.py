from datetime import UTC, datetime

from sqlalchemy.orm import sessionmaker

from calling_agent.domain.entities import Booking, Room
from calling_agent.domain.repositories import BookingRepository, RoomRepository
from core.exceptions.exceptions_decorators import handle_service_exceptions
from core.logging.logger import setup_logger
from utils.database.models import BookingModel, RoomModel

logger = setup_logger(__name__)


def _as_utc(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        return moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)


def _to_room(model: RoomModel) -> Room:
    return Room(code=model.code, capacity=model.capacity)


def _to_booking(model: BookingModel) -> Booking:
    return Booking(
        id=model.id,
        room_code=model.room_code,
        user_id=model.user_id,
        title=model.title,
        attendees=model.attendees,
        start_time=_as_utc(model.start_time),
        end_time=_as_utc(model.end_time),
    )


class SqlAlchemyRoomRepository(RoomRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    @handle_service_exceptions(logger)
    def get_all(self) -> list[Room]:
        with self._session_factory() as session:
            return [_to_room(m) for m in session.query(RoomModel).all()]

    @handle_service_exceptions(logger)
    def get_by_code(self, code: str) -> Room | None:
        with self._session_factory() as session:
            model = session.get(RoomModel, code)
            return _to_room(model) if model else None


class SqlAlchemyBookingRepository(BookingRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    @handle_service_exceptions(logger)
    def add(self, booking: Booking) -> Booking:
        with self._session_factory() as session:
            model = BookingModel(
                room_code=booking.room_code,
                user_id=booking.user_id,
                title=booking.title,
                attendees=booking.attendees,
                start_time=_as_utc(booking.start_time),
                end_time=_as_utc(booking.end_time),
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _to_booking(model)

    @handle_service_exceptions(logger)
    def get_by_id(self, booking_id: int) -> Booking | None:
        with self._session_factory() as session:
            model = session.get(BookingModel, booking_id)
            return _to_booking(model) if model else None

    @handle_service_exceptions(logger)
    def list_for_room_between(self, room_code: str, start: datetime, end: datetime) -> list[Booking]:
        with self._session_factory() as session:
            models = (
                session.query(BookingModel)
                .filter(
                    BookingModel.room_code == room_code,
                    BookingModel.start_time < end,
                    BookingModel.end_time > start,
                )
                .all()
            )
            return [_to_booking(m) for m in models]

    @handle_service_exceptions(logger)
    def list_for_user(self, user_id: str) -> list[Booking]:
        with self._session_factory() as session:
            models = (
                session.query(BookingModel)
                .filter(BookingModel.user_id == user_id)
                .order_by(BookingModel.start_time)
                .all()
            )
            return [_to_booking(m) for m in models]

    @handle_service_exceptions(logger)
    def delete(self, booking_id: int) -> None:
        with self._session_factory() as session:
            model = session.get(BookingModel, booking_id)
            if model is not None:
                session.delete(model)
                session.commit()
