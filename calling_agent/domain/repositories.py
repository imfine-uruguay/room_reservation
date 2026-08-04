from abc import ABC, abstractmethod
from datetime import datetime

from calling_agent.domain.entities import Booking, Room


class RoomRepository(ABC):
    """Port for read access to the fixed set of meeting rooms."""

    @abstractmethod
    def get_all(self) -> list[Room]: ...

    @abstractmethod
    def get_by_code(self, code: str) -> Room | None: ...


class BookingRepository(ABC):
    """Port for persisting and querying bookings."""

    @abstractmethod
    def add(self, booking: Booking) -> Booking: ...

    @abstractmethod
    def get_by_id(self, booking_id: int) -> Booking | None: ...

    @abstractmethod
    def list_for_room_between(self, room_code: str, start: datetime, end: datetime) -> list[Booking]: ...

    @abstractmethod
    def list_for_user(self, user_id: str) -> list[Booking]: ...

    @abstractmethod
    def delete(self, booking_id: int) -> None: ...
