from datetime import datetime
from typing import Callable

from regta_period import Period


def _assert_creation(f: Callable[..., Period], reverse: bool = False):
    try:
        f()
    except ValueError:
        assert reverse
    else:
        assert not reverse


def test_wrong_combination_of_time_and_interval():
    _assert_creation(lambda: Period().every(12).hours.at("12:00"), reverse=True)
    _assert_creation(lambda: Period().every(12).hours.at("24:00"), reverse=True)
    _assert_creation(lambda: Period().every(2).days.AND.every(12).hours.at("12:00"), reverse=True)
    _assert_creation(lambda: Period().every(2).days.AND.every(12).hours.at("00:00"), reverse=True)


def test_correct_combination_of_time_and_interval():
    _assert_creation(lambda: Period().every(2).days.at("12:00"))
    _assert_creation(lambda: Period().every(24).hours.at("12:12"))
    _assert_creation(lambda: Period().every(24).hours.at("24:00"))


def test_at_time(unix: datetime):
    p = Period().every(3).days.at("12:00")
    moment = datetime(year=1970, month=1, day=1, hour=12, minute=0, second=0)
    assert p.get_next_datetime(unix) == moment
    next_moment = datetime(year=1970, month=1, day=1+3, hour=12, minute=0, second=0)
    assert p.get_next_datetime(moment) == next_moment
    moment = next_moment
    next_moment = datetime(year=1970, month=1, day=1+6, hour=12, minute=0, second=0)
    assert p.get_next_datetime(moment) == next_moment

    p = Period().every(7).days.at("16:30:30")
    moment = datetime(year=1970, month=1, day=1, hour=16, minute=30, second=30)
    assert p.get_next_datetime(unix) == moment
    next_moment = datetime(year=1970, month=1, day=1+7, hour=16, minute=30, second=30)
    assert p.get_next_datetime(moment) == next_moment
    moment = next_moment
    next_moment = datetime(year=1970, month=1, day=1+14, hour=16, minute=30, second=30)
    assert p.get_next_datetime(moment) == next_moment
