# pylint: disable=protected-access
from datetime import datetime

from regta_period import Period, Weekdays


def test_creation():
    p = Period().on.monday
    assert p._weekdays == {Weekdays.MONDAY}
    p = Period().on.tuesday.AND.thursday.at("14:30").by("Asia/Tomsk")
    assert p._weekdays == {Weekdays.TUESDAY, Weekdays.THURSDAY}
    p = Period(weekdays=[Weekdays.WEDNESDAY])
    assert p._weekdays == {Weekdays.WEDNESDAY}
    p = Period().on.friday.AND.sunday.at("14:30")
    assert p._weekdays == {Weekdays.FRIDAY, Weekdays.SUNDAY}


def test_calculations():
    dt = datetime(2022, 7, 24, 0, 0, 0, 0)
    p1 = Period().on.monday.at("14:30")
    assert p1.get_next_datetime(dt) == datetime(2022, 7, 25, 14, 30, 0, 0)
    p2 = Period().on.tuesday.at("14:30")
    assert p2.get_next_datetime(dt) == datetime(2022, 7, 26, 14, 30, 0, 0)
    p2 = Period().on.wednesday.at("14:30")
    assert p2.get_next_datetime(dt) == datetime(2022, 7, 27, 14, 30, 0, 0)
    p2 = Period().on.thursday.at("14:30")
    assert p2.get_next_datetime(dt) == datetime(2022, 7, 28, 14, 30, 0, 0)
    p2 = Period().on.friday.at("14:30")
    assert p2.get_next_datetime(dt) == datetime(2022, 7, 29, 14, 30, 0, 0)
    p2 = Period().on.saturday.at("14:30")
    assert p2.get_next_datetime(dt) == datetime(2022, 7, 30, 14, 30, 0, 0)
    p2 = Period().on.sunday.at("14:30")
    assert p2.get_next_datetime(dt) == datetime(2022, 7, 24, 14, 30, 0, 0)


def test_weekdays_and_weekends():
    weekdays = {Weekdays.MONDAY, Weekdays.TUESDAY, Weekdays.WEDNESDAY, Weekdays.THURSDAY, Weekdays.FRIDAY}
    assert Period().weekdays._weekdays == weekdays
    weekends = {Weekdays.SATURDAY, Weekdays.SUNDAY}
    assert Period().weekends._weekdays == weekends
    assert Period().on.weekends.AND.monday._weekdays == (weekends | {Weekdays.MONDAY})
