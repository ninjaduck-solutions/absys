import datetime

from django.utils import timezone


def get_betrachtungszeitraum(jahr, eintritt):
    """
    Gibt den Beginn des Betrachtungszeitraums für das angegebene Jahr zurück.

    Beginnn ist entweder am 1.1. des angegebenen Jahres oder am
    Eintrittsdatum, wenn dieses im angegebenen Jahr liegt.
    """
    beginn = timezone.make_aware(datetime.datetime(jahr, 1, 1)).date()
    if eintritt.year == jahr:
        beginn = eintritt
    return beginn
