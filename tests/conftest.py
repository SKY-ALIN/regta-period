from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

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
