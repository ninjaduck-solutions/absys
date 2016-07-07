import datetime

import pytest
from pytest_factoryboy import register

from . import factories


register(factories.SchliesstagFactory)


@pytest.fixture
def betreuungstage_start():
    return datetime.date(2016, 7, 11)


@pytest.fixture
def betreuungstage_ende():
    return datetime.date(2016, 7, 17)
