from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimeSlot:
    """An immutable [start, end) time range used to validate bookings."""

    start: datetime
    end: datetime

    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end

    def is_block_aligned(self, block_minutes: int) -> bool:
        """True if both start and end fall exactly on a block boundary."""
        return (
            self.start.second == 0
            and self.start.microsecond == 0
            and self.start.minute % block_minutes == 0
            and self.end.second == 0
            and self.end.microsecond == 0
            and self.end.minute % block_minutes == 0
        )
