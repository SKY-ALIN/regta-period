from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest


@pytest.fixture
def unix():
    return datetime.utcfromtimestamp(0)


@pytest.fixture
def utc():
    return timezone.utc


@pytest.fixture
def utc7():
    return ZoneInfo('Asia/Tomsk')
