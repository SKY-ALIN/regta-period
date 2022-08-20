from datetime import datetime
from enum import Enum, unique


@unique
class Weekdays(Enum):
    """An enumeration of weekdays for the time windows logic."""

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def get(cls, dt: datetime) -> "Weekdays":
        """Create a :class:`Weekdays` object by a datetime object."""
        return cls(dt.weekday())
