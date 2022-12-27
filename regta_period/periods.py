from typing import Dict, Iterable, Set, Tuple, Union

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone as datetime_timezone, tzinfo

try:
    import zoneinfo  # type: ignore
except ImportError:  # Backward compatibility for python < 3.9
    from backports import zoneinfo  # type: ignore

from .enums import Weekdays

utc = datetime_timezone.utc


class AbstractPeriod(ABC):
    """The minimum interface every period object has."""

    @abstractmethod
    def get_interval(self, dt: datetime) -> timedelta:
        """Get time to the next moment as timedelta since passed moment.

        Args:
            dt (datetime): Current moment (:math:`t`)

        Return:
            timedelta: Interval to the next moment (:math:`f(t)`)
        """
        raise NotImplementedError

    @abstractmethod
    def get_next(self, dt: datetime) -> datetime:
        """Get the next moment since passed moment.

        Args:
            dt (datetime): Current moment (:math:`t`)

        Return:
            datetime: The next moment (:math:`t + f(t)`)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_timezone_in_use(self) -> bool:
        """If timezone is specified, return True, else False."""
        raise NotImplementedError


class Period(AbstractPeriod):
    """The core logic of this module.

    Args:
        days (int): Amount of days for the regular offset.
        hours (int): Amount of hours for the regular offset.
        minutes (int): Amount of minutes for the regular offset.
        seconds (int): Amount of seconds for the regular offset.
        milliseconds (int): Amount of milliseconds for the regular offset.
        time (str): Exact time of moments (time offset). Format: "HH:MM" or "HH:MM:SS".
        timezone (Union[tzinfo, str, int, float]):
            Time zone for exact time.
            If :obj:`str`, then it will be converted into :obj:`tzinfo` via :class:`zoneinfo.ZoneInfo`.
            If :obj:`int` or :obj:`float`, then it will be used directly as an offset for the time offset.
        weekdays (Iterable[Weekdays]): Time windows of weekdays.
    """

    _every: int = 1
    _regular_offset: float = 0.0
    _time_offset: int = 0
    _timezone_offset: Union[int, None] = None
    _timezone: Union[tzinfo, None] = None
    _weekdays: Set[Weekdays]

    def __init__(
            self,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
            milliseconds: int = 0,
            time: Union[str, None] = None,
            timezone: Union[tzinfo, str, int, float, None] = None,
            weekdays: Union[Iterable[Weekdays], None] = None,
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
        if timezone is not None:
            self._set_timezone(timezone)
        self._weekdays = set(weekdays) if weekdays is not None else set()

    def every(self, n: int) -> "Period":
        """Specify a factor for regular offset properties.

        Args:
            n (int): The factor.
        """
        self._every = n
        return self

    @property
    def seconds(self) -> "Period":
        """Seconds regular offset property. Must be used only after :attr:`.every` multiplier."""
        self._regular_offset += self._every
        return self

    @property
    def minutes(self) -> "Period":
        """Minutes regular offset property. Must be used only after :attr:`.every` multiplier."""
        self._regular_offset += self._every * 60
        return self

    @property
    def hours(self) -> "Period":
        """Hours regular offset property. Must be used only after :attr:`.every` multiplier."""
        self._regular_offset += self._every * 60 * 60
        return self

    @property
    def days(self) -> "Period":
        """Days regular offset property. Must be used only after :attr:`.every` multiplier."""
        self._regular_offset += self._every * 60 * 60 * 24
        return self

    @property
    def hourly(self) -> "Period":
        """Regular offset = every hour. The same as :code:`.every(1).hours`.
        Can't be combined with another regular offset.
        """
        if self._regular_offset:
            raise ValueError("Can't combine .hourly and other regular offset attributes")
        self._regular_offset = 60.0 * 60
        return self

    @property
    def daily(self) -> "Period":
        """Regular offset = every day. The same as :code:`.every(1).days`.
        Can't be combined with another regular offset.
        """
        if self._regular_offset:
            raise ValueError("Can't combine .daily and other regular offset attributes")
        self._regular_offset = 60.0 * 60 * 24
        return self

    @property
    def on(self) -> "Period":
        """This property does nothing. It's designed only to write better
        human-readable code, e.g. :code:`.on.monday`.
        """
        return self

    @property
    def monday(self) -> "Period":
        """Add Monday to the time windows list."""
        self._weekdays.add(Weekdays.MONDAY)
        return self

    @property
    def tuesday(self) -> "Period":
        """Add Tuesday to the time windows list."""
        self._weekdays.add(Weekdays.TUESDAY)
        return self

    @property
    def wednesday(self) -> "Period":
        """Add Wednesday to the time windows list."""
        self._weekdays.add(Weekdays.WEDNESDAY)
        return self

    @property
    def thursday(self) -> "Period":
        """Add Thursday to the time windows list."""
        self._weekdays.add(Weekdays.THURSDAY)
        return self

    @property
    def friday(self) -> "Period":
        """Add Friday to the time windows list."""
        self._weekdays.add(Weekdays.FRIDAY)
        return self

    @property
    def saturday(self) -> "Period":
        """Add Saturday to the time windows list."""
        self._weekdays.add(Weekdays.SATURDAY)
        return self

    @property
    def sunday(self) -> "Period":
        """Add Sunday to the time windows list."""
        self._weekdays.add(Weekdays.SUNDAY)
        return self

    @property
    def weekdays(self) -> "Period":
        """Add weekdays (Monday-Friday) to the time windows list."""
        self._weekdays.update({
            Weekdays.MONDAY,
            Weekdays.TUESDAY,
            Weekdays.WEDNESDAY,
            Weekdays.THURSDAY,
            Weekdays.FRIDAY,
        })
        return self

    @property
    def weekends(self) -> "Period":
        """Add weekends (Saturday-Sunday) to the time windows list."""
        self._weekdays.update({Weekdays.SATURDAY, Weekdays.SUNDAY})
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
                "Can't combine .at method and too small regular offset. "
                "Don't combine attributes which are < day with .at time method."
            )

        self._time_offset = hour * 60 * 60 + minute * 60 + second

    def at(self, time: str) -> "Period":
        """Specify the moment exact time (time offset, :math:`\Delta t_{time}`).

        Args:
            time (str): Exact time. Format: "HH:MM" or "HH:MM:SS".
        """
        self._set_time_offset(*self._parse_time(time))
        return self

    def _set_timezone(self, timezone: Union[tzinfo, str, int, float]) -> None:
        if isinstance(timezone, tzinfo):
            self._timezone = timezone
        elif isinstance(timezone, str):
            self._timezone = zoneinfo.ZoneInfo(timezone)
        elif isinstance(timezone, (int, float)):
            self._timezone_offset = int(timezone * 60 * 60)
        else:
            raise ValueError("Unsupported timezone type")

    def by(self, timezone: Union[tzinfo, str, int, float]) -> "Period":
        """Specify the time zone for the exact time.

        Args:
            timezone (Union[tzinfo, str, int, float]):
                Time zone.
                If :obj:`str`, then it will be converted into :obj:`tzinfo` via :class:`zoneinfo.ZoneInfo`.
                If :obj:`int` or :obj:`float`, then it will be used directly as an offset for the time offset.
        """
        self._set_timezone(timezone)
        return self

    def _get_initial_datetime(self) -> datetime:
        if self._timezone is not None:
            return datetime.fromtimestamp(self._time_offset, tz=utc).replace(tzinfo=self._timezone)
        if self._timezone_offset is not None:
            return datetime.fromtimestamp(self._time_offset - self._timezone_offset, tz=utc)
        return datetime.utcfromtimestamp(self._time_offset)

    def get_next(self, dt: datetime) -> datetime:
        delta_t = (dt - self._get_initial_datetime()).total_seconds()
        # if _regular_offset is not specified, calculate as .daily
        regular_offset = self._regular_offset or 60.0 * 60 * 24
        next_seconds = regular_offset - (delta_t % regular_offset)

        res = dt + timedelta(seconds=next_seconds)

        if self._weekdays and Weekdays.get(res) not in self._weekdays:
            return self.get_next(res)

        return res

    def get_interval(self, dt: datetime) -> timedelta:
        return self.get_next(dt) - dt

    @property
    def is_timezone_in_use(self) -> bool:
        return self._timezone is not None or self._timezone_offset is not None

    @property
    def AND(self) -> "Period":
        """This property does nothing. It's designed only to write better
        human-readable code, e.g. :code:`.on.monday.AND.tuesday`.
        It's uppercase because :code:`and` is a reserved word in python.
        """
        return self

    @property
    def OR(self) -> "PeriodAggregation":
        """Create :class:`PeriodAggregation` from this period and a new empty period.

        It's designed to write better human-readable code,
        e.g. :code:`.on.weekdays.at("18:00").OR.on.weekends.at("21:00")`.
        It's uppercase because :code:`or` is a reserved word in python.
        """
        return PeriodAggregation(self, Period())

    def __add__(self, other: "Period") -> "Period":
        """Combine periods as a sum of regular offset and time windows.
        Can't sum objects with a different time offset and time zone.
        """
        if self._time_offset != other._time_offset:
            raise ValueError(
                "Can't sum periods with a different time. "
                "Hint: try to use | instead"
            )
        if self._timezone != other._timezone or self._timezone_offset != other._timezone_offset:
            raise ValueError(
                "Can't sum periods with a different timezone. "
                "Hint: try to use an operator `|` or property `.OR` instead"
            )
        self._regular_offset += other._regular_offset
        self._weekdays.update(other._weekdays)
        return self

    def __or__(self, other: Union["Period", "PeriodAggregation"]) -> "PeriodAggregation":
        """Create new :class:`PeriodAggregation` from this period and the passed period."""
        if isinstance(other, Period):
            return PeriodAggregation(self, other)
        return PeriodAggregation(self, *other.periods)

    def __repr__(self):
        data: Dict[str, str] = {
            "regular_offset": f"{self._regular_offset or 60.0 * 60 * 24}s",
            "time_offset": f"{self._time_offset}s",
        }
        if self._timezone is not None:
            data["timezone"] = str(self._timezone)
        elif self._timezone_offset is not None:
            data["timezone_offset"] = f"{self._timezone_offset}s"
        if self._weekdays:
            data["weekdays"] = ",".join(map(lambda x: x.name.capitalize(), self._weekdays))

        data_str = ", ".join(f"{key}={value}" for key, value in data.items())
        return f"<{self.__class__.__name__}: {data_str}>"


class PeriodAggregation(AbstractPeriod):
    """Aggregation class for :class:`Period`.

    It contains the logic of how to get the nearest time moment and add data into
    the last period object.

    Args:
        *periods (Tuple[Period]): Periods to aggregate.

    Attributes:
        periods (Tuple[Period]): Aggregated periods.
    """

    def __init__(self, *periods: Period):
        if not periods:
            raise ValueError("No period has been passed")
        self.periods = periods

    def get_next(self, dt: datetime) -> datetime:
        return min(map(lambda period: period.get_next(dt), self.periods))

    def get_interval(self, dt: datetime) -> timedelta:
        return self.get_next(dt) - dt

    @property
    def is_timezone_in_use(self) -> bool:
        return any(map(lambda period: period.is_timezone_in_use, self.periods))

    @property
    def OR(self) -> "PeriodAggregation":
        """Create a new :class:`PeriodAggregation` from these periods of
        aggregation and a new empty period.

        It's designed to write better human-readable code,
        e.g. :code:`.on.weekdays.at("18:00").OR.on.weekends.at("21:00")`.
        It's uppercase because :code:`or` is a reserved word in python.
        """
        return PeriodAggregation(*self.periods, Period())

    def __or__(self, other: Union["Period", "PeriodAggregation"]) -> "PeriodAggregation":
        """Create a new :class:`PeriodAggregation` from these periods of
        aggregation and the passed period."""
        if isinstance(other, Period):
            return PeriodAggregation(*self.periods, other)
        return PeriodAggregation(*self.periods, *other.periods)

    def __dir__(self) -> Iterable[str]:
        """Extended implementation of the standard.
        It adds attributes of :class:`Period` class.
        """
        return sorted(set(dir(PeriodAggregation)) | set(dir(Period)))

    def __getattr__(self, attr):
        """Return an attribute of the last period in the list of periods with
        a wrap to return this object instead of the last period.
        """
        _attr = getattr(self.periods[-1], attr)

        if isinstance(getattr(Period, attr), property):
            return self

        def wrapper(*args, **kwargs):
            _attr(*args, **kwargs)
            return self

        return wrapper

    def __repr__(self):
        return f"<{self.__class__.__name__}: {' OR '.join(map(repr, self.periods))}>"
