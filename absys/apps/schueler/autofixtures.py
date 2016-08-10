from datetime import timedelta

from autofixture import AutoFixture, generators, register
from django.utils import timezone
from faker import Factory

from . import models

fake = Factory.create()


class SchuelerAutoFixture(AutoFixture):

    field_values = {
        'vorname': generators.CallableGenerator(fake.first_name),
        'nachname': generators.CallableGenerator(fake.last_name),
        'geburtsdatum': generators.DateGenerator(
            min_date=timezone.now().date() - timedelta(365 * 20),
            max_date=timezone.now().date() - timedelta(365 * 10)
        ),
    }


register(models.Schueler, SchuelerAutoFixture)
