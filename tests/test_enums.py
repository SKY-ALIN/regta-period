from datetime import datetime

from regta_period.enums import Weekdays


def test_weekdays():
    assert Weekdays.get(datetime(2022, 7, 24, 0, 0, 0)) == Weekdays.SUNDAY
    assert Weekdays.get(datetime(2022, 7, 25, 0, 0, 0)) == Weekdays.MONDAY
    assert Weekdays.get(datetime(2022, 7, 26, 0, 0, 0)) == Weekdays.TUESDAY
    assert Weekdays.get(datetime(2022, 7, 27, 0, 0, 0)) == Weekdays.WEDNESDAY
    assert Weekdays.get(datetime(2022, 7, 28, 0, 0, 0)) == Weekdays.THURSDAY
    assert Weekdays.get(datetime(2022, 7, 29, 0, 0, 0)) == Weekdays.FRIDAY
    assert Weekdays.get(datetime(2022, 7, 30, 0, 0, 0)) == Weekdays.SATURDAY
