from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Tuple, Optional


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
    3. [Done] At specific time.

    Todo:
        [] Add `.daily`
        [] Add timezone support `.by(+1)`, `.by(-7)` and so on
    """

    _epoch: datetime = datetime.utcfromtimestamp(0)
    _regular_offset: float = 0.0
    _every: int = 1

    def __init__(
            self,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
            milliseconds: int = 0,
            time: Optional[str] = None,
    ):
        self._regular_offset = (
            milliseconds * 0.001
            + seconds
            + minutes * 60
            + hours * 60 * 60
            + days * 60 * 60 * 24
        )
        if time is not None:
            self._set_time_offset(*self._parse_time(time))

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

    @staticmethod
    def _parse_time(time: str) -> Tuple[int, int, int]:
        values = tuple(map(int, time.split(":")))

        if len(values) == 2:
            hour, minute = values
            second = 0
        elif len(values) == 3:
            hour, minute, second = values
        else:
            raise ValueError(f"Wrong time format: {repr(time)}")

        return hour, minute, second

    def _set_time_offset(self, hour: int, minute: int, second: int) -> None:
        checking_delimiter = (24 * 60 * 60)
        if self._regular_offset % checking_delimiter:
            raise ValueError(
                "Can't combine .at method and regular interval. Regular interval is too small. "
                "Don't combine intervals which are < days with .at time method."
            )

        offset = hour * 60 * 60 + minute * 60 + second
        self._epoch = datetime.utcfromtimestamp(offset)

    def at(self, time: str) -> "Period":
        self._set_time_offset(*self._parse_time(time))
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
