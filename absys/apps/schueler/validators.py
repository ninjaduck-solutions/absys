from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_geburtsdatum_in_vergangenheit(value):
    """
    Überprüft, dass ein Geburtsdatum in der Vergangenheit liegt.
    """
    if value > now().date():
        raise ValidationError(
            "Das Geburtsdatum darf nicht in der Zukunft liegen.",
            code='geburtsdatum_in_zukunft'
        )
