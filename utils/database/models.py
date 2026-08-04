from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class RoomModel(Base):
    __tablename__ = "rooms"

    code = Column(String(1), primary_key=True)
    capacity = Column(Integer, nullable=False)


class BookingModel(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("attendees > 0", name="ck_bookings_attendees_positive"),
        CheckConstraint("end_time > start_time", name="ck_bookings_end_after_start"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_code = Column(String(1), ForeignKey("rooms.code"), nullable=False, index=True)
    user_id = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    attendees = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
