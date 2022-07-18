from datetime import datetime

from regta_period import Period


def test_wrong_combination_of_time_and_interval():
    try:
        Period().every(12).hours.at("12:00")
    except ValueError:
        assert True
    else:
        assert False

    try:
        Period().every(12).hours.at("24:00")
    except ValueError:
        assert True
    else:
        assert False

    try:
        Period().every(2).days.AND.every(12).hours.at("12:00")
    except ValueError:
        assert True
    else:
        assert False

    try:
        Period().every(2).days.AND.every(12).hours.at("00:00")
    except ValueError:
        assert True
    else:
        assert False


def test_correct_combination_of_time_and_interval():
    try:
        Period().every(2).days.at("12:00")
    except ValueError:
        assert False
    else:
        assert True

    try:
        Period().every(24).hours.at("12:12")
    except ValueError:
        assert False
    else:
        assert True

    try:
        Period().every(24).hours.at("24:00")
    except ValueError:
        assert False
    else:
        assert True


def test_at_time(unix: datetime):
    p = Period().every(3).days.at("12:00")
    moment = datetime(year=1970, month=1, day=1, hour=12, minute=0, second=0)
    assert p.get_next_datetime(unix) == moment
    next_moment = datetime(year=1970, month=1, day=1+3, hour=12, minute=0, second=0)
    assert (p.get_next_datetime(moment) == next_moment)
    moment = next_moment
    next_moment = datetime(year=1970, month=1, day=1+6, hour=12, minute=0, second=0)
    assert (p.get_next_datetime(moment) == next_moment)

    p = Period().every(7).days.at("16:30:30")
    moment = datetime(year=1970, month=1, day=1, hour=16, minute=30, second=30)
    assert p.get_next_datetime(unix) == moment
    next_moment = datetime(year=1970, month=1, day=1+7, hour=16, minute=30, second=30)
    assert (p.get_next_datetime(moment) == next_moment)
    moment = next_moment
    next_moment = datetime(year=1970, month=1, day=1+14, hour=16, minute=30, second=30)
    assert (p.get_next_datetime(moment) == next_moment)
