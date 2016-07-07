import datetime

import pytest


@pytest.fixture
def betreuungstage_start():
    return datetime.date(2016, 7, 11)


@pytest.fixture
def betreuungstage_ende():
    return datetime.date(2016, 7, 17)
