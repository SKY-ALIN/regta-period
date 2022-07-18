from datetime import datetime, timedelta

from regta_period import Period


def test_by_every_setup():
    s1 = 3 * 60 * 60 + 30 * 60 - 15
    dt1 = datetime.utcfromtimestamp(s1)
    s2 = 3 * 60 * 60 + 30 * 60
    dt2 = datetime.utcfromtimestamp(s2)

    p = Period().every(3).hours.AND.every(30).minutes
    assert p.get_next_seconds(dt1) == 15
    assert p.get_next_timedelta(dt1) == timedelta(seconds=15)
    assert p.get_next_datetime(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_next_seconds(dt2) == s2
    assert p.get_next_timedelta(dt2) == timedelta(seconds=s2)
    assert p.get_next_datetime(dt2) == dt2 + timedelta(seconds=s2)

    # The same, but with __and__ magic method
    p = Period().every(3).hours & Period().every(30).minutes
    assert p.get_next_seconds(dt1) == 15
    assert p.get_next_timedelta(dt1) == timedelta(seconds=15)
    assert p.get_next_datetime(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_next_seconds(dt2) == s2
    assert p.get_next_timedelta(dt2) == timedelta(seconds=s2)
    assert p.get_next_datetime(dt2) == dt2 + timedelta(seconds=s2)


def test_by_init_setup():
    s1 = 3 * 60 * 60 + 30 * 60 - 15
    dt1 = datetime.utcfromtimestamp(s1)
    s2 = 3 * 60 * 60 + 30 * 60
    dt2 = datetime.utcfromtimestamp(s2)

    p = Period(hours=3, minutes=30)
    assert p.get_next_seconds(dt1) == 15
    assert p.get_next_timedelta(dt1) == timedelta(seconds=15)
    assert p.get_next_datetime(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_next_seconds(dt2) == s2
    assert p.get_next_timedelta(dt2) == timedelta(seconds=s2)
    assert p.get_next_datetime(dt2) == dt2 + timedelta(seconds=s2)

    # The same, but with __and__ magic method
    p = Period(hours=3) & Period(minutes=30)
    assert p.get_next_seconds(dt1) == 15
    assert p.get_next_timedelta(dt1) == timedelta(seconds=15)
    assert p.get_next_datetime(dt1) == dt1 + timedelta(seconds=15)

    assert p.get_next_seconds(dt2) == s2
    assert p.get_next_timedelta(dt2) == timedelta(seconds=s2)
    assert p.get_next_datetime(dt2) == dt2 + timedelta(seconds=s2)
