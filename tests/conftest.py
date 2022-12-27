from datetime import datetime, timezone

try:
    import zoneinfo
except ImportError:  # Backward compatibility for python < 3.9
    from backports import zoneinfo  # type: ignore

import pytest


@pytest.fixture
def unix():
    return datetime.utcfromtimestamp(0)


@pytest.fixture
def utc():
    return timezone.utc


@pytest.fixture
def utc7():
    return zoneinfo.ZoneInfo('Asia/Tomsk')
