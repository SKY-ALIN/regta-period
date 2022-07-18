from datetime import datetime

import pytest


@pytest.fixture
def unix():
    return datetime.utcfromtimestamp(0)
