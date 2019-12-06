import arrow
import pytest

from absys.apps.einrichtungen import configurations


@pytest.mark.django_db
class TestEinrichtungKonfiguration365:

    def test_fehltage_letzte_rechnung(
            self, schueler, einrichtung, rechnungs_position_schueler_factory, einrichtung_factory):
        letzte_rechnung = (arrow.Arrow(2016, 6, 10), arrow.Arrow(2016, 6, 14))
        startdatum = letzte_rechnung[1].shift(days=+1).date()
        conf = configurations.registry[365]
        # Es existieren noch keine RechnungsPositionSchueler.
        assert conf.fehltage_letzte_rechnung(schueler, einrichtung, startdatum) == 0
        for datum in arrow.Arrow.range('day', *letzte_rechnung):
            rechnungs_position_schueler_factory.create(
                datum=datum.date(), schueler=schueler, einrichtung=einrichtung, abwesend=True
            )
        # Es existieren fünf RechnungsPositionSchueler als abwesende Tage.
        assert schueler.positionen_schueler.count() == 5
        # Wird das falsche Startdatum gewählt, wird nichts gefunden.
        assert conf.fehltage_letzte_rechnung(schueler, einrichtung, letzte_rechnung[0].date()) == 0
        # Mit dem richtigen Startdatum wird das Maximum gefunden.
        assert conf.fehltage_letzte_rechnung(schueler, einrichtung, startdatum) == 3
        # Wenn nur der erste Tag der letzten Rechnung ein Fehltag ist, werden
        # keine gefunden, da dieser nicht im Limit von drei Tagen liegt.
        schueler.positionen_schueler.exclude(datum=letzte_rechnung[0].date()).update(abwesend=False)
        assert conf.fehltage_letzte_rechnung(schueler, einrichtung, startdatum) == 0
        # Ist der letzte Tag der letzten Rechnung ein Fehltag, wird dieser
        # gefunden.
        schueler.positionen_schueler.update(abwesend=False)
        schueler.positionen_schueler.filter(datum=letzte_rechnung[1].date()).update(abwesend=True)
        assert conf.fehltage_letzte_rechnung(schueler, einrichtung, startdatum) == 1
        # Stimmt die Einrichtung nicht überein, wird nichts gefunden.
        schueler.positionen_schueler.update(einrichtung=einrichtung_factory())
        assert conf.fehltage_letzte_rechnung(schueler, einrichtung, startdatum) == 0

    def test_fehltage_folgezeitraum(self, schueler, anwesenheit_factory):
        folgezeitraum = (arrow.Arrow(2016, 6, 10), arrow.Arrow(2016, 6, 14))
        enddatum = folgezeitraum[0].shift(days=-1).date()
        conf = configurations.registry[365]
        # Es existieren noch keine Anwesenheiten.
        assert conf.fehltage_folgezeitraum(schueler, enddatum) == 0
        for datum in arrow.Arrow.range('day', *folgezeitraum):
            anwesenheit_factory.create(datum=datum.date(), schueler=schueler, abwesend=True)
        # Es existieren fünf Anwesenheiten als abwesende Tage.
        assert schueler.anwesenheit.count() == 5
        # Wird das falsche Enddatum gewählt, wird nichts gefunden.
        assert conf.fehltage_folgezeitraum(schueler, folgezeitraum[1].date()) == 0
        # Mit dem richtigen Enddatum wird das Maximum gefunden.
        assert conf.fehltage_folgezeitraum(schueler, enddatum) == 3
        # Wenn nur der letzte Tag des Folgezeitraums ein Fehltag ist, werden
        # keine gefunden, da dieser nicht im Limit von drei Tagen liegt.
        schueler.anwesenheit.exclude(datum=folgezeitraum[1].date()).update(abwesend=False)
        assert conf.fehltage_folgezeitraum(schueler, enddatum) == 0
        # Ist der erste Tag des Folgezeitraums ein Fehltag, wird dieser
        # gefunden.
        schueler.anwesenheit.update(abwesend=False)
        schueler.anwesenheit.filter(datum=folgezeitraum[0].date()).update(abwesend=True)
        assert conf.fehltage_folgezeitraum(schueler, enddatum) == 1
