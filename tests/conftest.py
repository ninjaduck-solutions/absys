# encoding: utf-8
import shutil
import tempfile
from functools import partial

import pytest
from faker import Faker
from pytest_factoryboy import register

from .abrechnung.factories import RechnungSozialamtFactory, RechnungsPositionSchuelerFactory
from .anwesenheitsliste.factories import AnwesenheitFactory
from .buchungskennzeichen.factories import BuchungskennzeichenFactory
from .einrichtungen.factories import (EinrichtungFactory, EinrichtungHatPflegesatzFactory,
    FerienFactory, BettengeldsatzFactory, SchuelerAngemeldetInEinrichtungFactory, SchuelerInEinrichtungFactory,
    StandortFactory, SchliesstagFactory)
from .schueler.factories import GruppeFactory, SchuelerFactory, SozialamtFactory
from .benachrichtigungen.factories import (BuchungskennzeichenBenachrichtigungFactory,
                                           SchuelerInEinrichtungLaeuftAusBenachrichtigungFactory,
                                           EinrichtungHatPflegesatzLaeuftAusBenachrichtigungFactory,
                                           BettengeldsatzLaeuftAusBenachrichtigungFactory,
                                           FerienBenachrichtigungFactory,
                                           SchliesstageBenachrichtigungFactory)

register(RechnungSozialamtFactory)
register(RechnungsPositionSchuelerFactory)
register(AnwesenheitFactory)
register(BuchungskennzeichenFactory)
register(EinrichtungFactory)
register(BettengeldsatzFactory)
register(EinrichtungHatPflegesatzFactory)
register(FerienFactory)
register(GruppeFactory)
register(SchuelerAngemeldetInEinrichtungFactory)
register(SchuelerFactory)
register(SchuelerInEinrichtungFactory)
register(SozialamtFactory)
register(StandortFactory)
register(SchliesstagFactory)
register(BuchungskennzeichenBenachrichtigungFactory)
register(SchuelerInEinrichtungLaeuftAusBenachrichtigungFactory)
register(EinrichtungHatPflegesatzLaeuftAusBenachrichtigungFactory)
register(BettengeldsatzLaeuftAusBenachrichtigungFactory)
register(FerienBenachrichtigungFactory)
register(SchliesstageBenachrichtigungFactory)


@pytest.fixture
def loaddata(settings, db):
    """Load a Django fixture.

    Works exactly like the loaddata command. All command line options must be
    given as keyword arguments.

    There is no no need to mark the test itself with the django_db marker
    because the loaddata fixture already loads the db fixture.

    Usage::

        def test_model(loaddata):
            loaddata('my_fixture')
            # do a test using the fixture


        def test_othermodel(loaddata):
            loaddata('other_fixture', database='other')
            # do a test using the fixture
    """
    from django.core import management
    return partial(management.call_command, 'loaddata')


def pytest_runtest_setup(item):
    """Seed the Faker generator for every test.

    Faker is seeded at the beginning of each test based on the test name, so
    each test that uses Faker will use the same fake data between test runs,
    regardless of test order.

    Requires Faker 0.5.3 or newer.
    """
    Faker().seed(item.nodeid)


@pytest.fixture
def tmp_media_root(request, settings):
    """Create a temporary directory and use it as MEDIA_ROOT.

    The temporary directory is deleted after the test has been finished.
    """
    settings.MEDIA_ROOT = tempfile.mkdtemp()
    settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    def cleanup():
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
    request.addfinalizer(cleanup)
