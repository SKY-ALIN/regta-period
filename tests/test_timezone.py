from datetime import datetime, timedelta

from regta_period import Period


def _assert(p_utc: Period, p_tomsk: Period, dt_utc: datetime, dt_tomsk: datetime):
    assert p_utc.get_interval(dt_utc) == timedelta(hours=1, minutes=30)  # UTC and UTC
    assert p_utc.get_interval(dt_tomsk) == timedelta(hours=8, minutes=30)  # UTC and UTC+7
    assert p_tomsk.get_interval(dt_utc) == timedelta(hours=18, minutes=30)  # UTC+7 and UTC
    assert p_tomsk.get_interval(dt_tomsk) == timedelta(hours=1, minutes=30)  # UTC+7 and UTC+7


def test_timezone_with_exact_time(utc, utc7):
    p_utc = Period(days=1).at("10:30").by(utc)
    dt_utc = datetime(year=2000, month=1, day=10, hour=9, minute=0, second=0, tzinfo=utc)
    p_tomsk = Period(days=1).at("10:30").by('Asia/Tomsk')  # UTC+7
    dt_tomsk = datetime(year=2000, month=1, day=10, hour=9, minute=0, second=0, tzinfo=utc7)
    _assert(p_utc, p_tomsk, dt_utc, dt_tomsk)


def test_timezone_as_number_with_exact_time(utc, utc7):
    p_utc = Period(days=1).at("10:30").by(0)  # UTC
    dt_utc = datetime(year=2000, month=1, day=10, hour=9, minute=0, second=0, tzinfo=utc)
    p_tomsk = Period(days=1).at("10:30").by(+7)  # UTC+7
    dt_tomsk = datetime(year=2000, month=1, day=10, hour=9, minute=0, second=0, tzinfo=utc7)
    _assert(p_utc, p_tomsk, dt_utc, dt_tomsk)
