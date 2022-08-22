from datetime import datetime, timedelta

from regta_period import Period, PeriodAggregation


def _assert(p: PeriodAggregation, dt):
    assert p.get_next(dt) == datetime(year=1970, month=1, day=1, hour=11, minute=0, second=0)
    assert p.get_interval(dt) == timedelta(hours=11)


def test_direct_creation(unix: datetime):
    p = PeriodAggregation(
        Period().daily.at("16:00"),
        Period().on.thursday.at("11:00"),
        Period().on.monday.at("9:00"),
    )
    _assert(p, unix)


def test_magic_creation(unix: datetime):
    p = Period().daily.at("16:00") | Period().on.thursday.at("11:00") | Period().on.monday.at("9:00")
    _assert(p, unix)


def test_dot_or_creation(unix: datetime):
    p = Period().daily.at("16:00").OR.on.thursday.at("11:00").OR.on.monday.at("9:00")
    _assert(p, unix)
