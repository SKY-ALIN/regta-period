from abc import ABC, abstractmethod
from datetime import datetime, timedelta, tzinfo, timezone as datetime_timezone
from typing import Tuple, Optional, Union
try:
    import zoneinfo
except ImportError:  # Backward compatibility for python < 3.9
    from backports import zoneinfo

utc = datetime_timezone.utc


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
        [Done] Add `.daily` and `.hourly`
        [Done] Add timezone support `.by(+1)`, `.by(-7)` and so on
    """

    _every: int = 1
    _regular_offset: float = 0.0
    _time_offset: int = 0
    _timezone_offset: Optional[int] = None
    _timezone: Optional[tzinfo] = None

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
    def hourly(self) -> "Period":
        if self._regular_offset:
            raise ValueError("Can't combine .hourly and other regular interval attributes")
        self._regular_offset = 60 * 60
        return self

    @property
    def daily(self) -> "Period":
        if self._regular_offset:
            raise ValueError("Can't combine .daily and other regular interval attributes")
        self._regular_offset = 60 * 60 * 24
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

        self._time_offset = hour * 60 * 60 + minute * 60 + second

    def at(self, time: str) -> "Period":
        self._set_time_offset(*self._parse_time(time))
        return self

    def by(self, timezone: Union[tzinfo, str, int, float]) -> "Period":
        if isinstance(timezone, tzinfo):
            self._timezone = timezone
        elif isinstance(timezone, str):
            self._timezone = zoneinfo.ZoneInfo(timezone)
        elif isinstance(timezone, (int, float)):
            self._timezone_offset = int(timezone * 60 * 60)
        else:
            raise ValueError("Unsupported timezone type")
        return self

    def _get_initial_offset(self) -> datetime:
        if self._timezone is not None:
            return datetime.fromtimestamp(self._time_offset, tz=utc).replace(tzinfo=self._timezone)
        if self._timezone_offset is not None:
            return datetime.fromtimestamp(self._time_offset - self._timezone_offset, tz=utc)
        return datetime.utcfromtimestamp(self._time_offset)

    def get_next_seconds(self, dt: datetime) -> float:
        delta_t = (dt - self._get_initial_offset()).total_seconds()
        return self._regular_offset - (delta_t % self._regular_offset)

    def get_next_timedelta(self, dt: datetime) -> timedelta:
        return timedelta(seconds=self.get_next_seconds(dt))

    def get_next_datetime(self, dt: datetime) -> datetime:
        return dt + self.get_next_timedelta(dt)

    def __repr__(self):
        timezone = (
            f", timezone={self._timezone}"
            if self._timezone is not None
            else f", timezone_offset={self._timezone_offset}s"
            if self._timezone_offset is not None
            else ""
        )
        return (
            f"<{self.__class__.__name__}: "
            f"regular_offset={self._regular_offset}s, "
            f"time_offset={self._time_offset}s{timezone}>"
        )


class PeriodAggregation(AbstractPeriod):
    pass
