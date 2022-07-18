from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class AbstractPeriod(ABC):
    @abstractmethod
    def get_next_seconds(self, dt: datetime) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_next_timedelta(self, dt: datetime) -> timedelta:
        raise NotImplementedError

    @abstractmethod
    def get_next_datetime(self, dt: datetime) -> datetime:
        raise NotImplementedError


class Period(AbstractPeriod):
    """There are 3 types of intervals approaches:
    1. [Done] Regular aka. days, minutes, months and so on.
    2. [] Calculated aka. Sun, Mon, August, September and so on.
    3. [] At specific time.
    """

    _epoch: datetime = datetime.utcfromtimestamp(0)
    _regular_offset: float = 0.0
    _every: int = 1

    def __init__(self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, milliseconds: int = 0):
        self._regular_offset = (
            milliseconds * 0.001
            + seconds
            + minutes * 60
            + hours * 60 * 60
            + days * 60 * 60 * 24
        )

    def every(self, n: int) -> "Period":
        self._every = n
        return self

    @property
    def seconds(self) -> "Period":
        self._regular_offset += self._every
        return self

    @property
    def minutes(self) -> "Period":
        self._regular_offset += self._every * 60
        return self

    @property
    def hours(self) -> "Period":
        self._regular_offset += self._every * 60 * 60
        return self

    @property
    def days(self) -> "Period":
        self._regular_offset += self._every * 60 * 60 * 24
        return self

    @property
    def AND(self) -> "Period":
        return self

    def __and__(self, other: "Period") -> "Period":
        self._regular_offset += other._regular_offset
        return self

    def get_next_seconds(self, dt: datetime) -> float:
        seconds_since_epoch = (dt - self._epoch).total_seconds()
        seconds_until_next = self._regular_offset - (seconds_since_epoch % self._regular_offset)
        return seconds_until_next

    def get_next_timedelta(self, dt: datetime) -> timedelta:
        return timedelta(seconds=self.get_next_seconds(dt))

    def get_next_datetime(self, dt: datetime) -> datetime:
        return dt + self.get_next_timedelta(dt)


class PeriodAggregation(AbstractPeriod):
    pass
