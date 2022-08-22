from datetime import datetime, timedelta

from regta_period import Period

from .test_at_time import _assert_creation


def test_by_every_setup():
    s1 = 3 * 60 * 60 + 30 * 60 - 15
    dt1 = datetime.utcfromtimestamp(s1)
    s2 = 3 * 60 * 60 + 30 * 60
    dt2 = datetime.utcfromtimestamp(s2)

    p = Period().every(3).hours.AND.every(30).minutes
    assert p.get_interval(dt1) == timedelta(seconds=15)
    assert p.get_next(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_interval(dt2) == timedelta(seconds=s2)
    assert p.get_next(dt2) == dt2 + timedelta(seconds=s2)

    # The same, but with __and__ magic method
    p = Period().every(3).hours + Period().every(30).minutes
    assert p.get_interval(dt1) == timedelta(seconds=15)
    assert p.get_next(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_interval(dt2) == timedelta(seconds=s2)
    assert p.get_next(dt2) == dt2 + timedelta(seconds=s2)


def test_by_init_setup():
    s1 = 3 * 60 * 60 + 30 * 60 - 15
    dt1 = datetime.utcfromtimestamp(s1)
    s2 = 3 * 60 * 60 + 30 * 60
    dt2 = datetime.utcfromtimestamp(s2)

    p = Period(hours=3, minutes=30)
    assert p.get_interval(dt1) == timedelta(seconds=15)
    assert p.get_next(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_interval(dt2) == timedelta(seconds=s2)
    assert p.get_next(dt2) == dt2 + timedelta(seconds=s2)

    # The same, but with __and__ magic method
    p = Period(hours=3) + Period(minutes=30)
    assert p.get_interval(dt1) == timedelta(seconds=15)
    assert p.get_next(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_interval(dt2) == timedelta(seconds=s2)
    assert p.get_next(dt2) == dt2 + timedelta(seconds=s2)


def test_daily_and_hourly():
    _assert_creation(lambda: Period().daily.hourly, reverse=True)
    _assert_creation(lambda: Period().every(3).minutes.hourly, reverse=True)
    _assert_creation(lambda: Period().every(3).minutes.daily, reverse=True)

    s = 3 * 60 * 60 - 15
    dt = datetime.utcfromtimestamp(s)

    assert Period().hourly.get_interval(dt) == timedelta(seconds=15)
    assert Period().daily.get_interval(dt) == timedelta(hours=21, minutes=0, seconds=15)
