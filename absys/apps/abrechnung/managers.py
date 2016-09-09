from datetime import datetime

from django.db import models, transaction
from django.utils import timezone


class RechnungSozialamtManager(models.Manager):

    @transaction.atomic
    def rechnungslauf(self, sozialamt, startdatum, enddatum):
        """
        Erzeugt eine ``RechnungSchueler`` pro Schüler des Sozialamts im gewählten Zeitraum.

        1. Erstellen oder Aktualisieren einer ``RechnungSchueler``-Instanz pro Schüler.
        2. Abwesenheitstage pro Schüler im gewählten Zeitraum ermitteln.
        3. Für jeden Betreuungstag im gewählten Zeitraum pro Schüler eine ``RechnungsPositionSchueler`` erstellen und wenn nötig mit passender ``RechnungSchueler``-Instanz verknüpfen.
        4. Noch nicht abgerechnete ``RechnungsPositionSchueler``-Instanzen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.
        5. ``RechnungSchueler``-Instanz pro Schüler aktualisieren (Summe und Fehltage).
        """
        from .models import RechnungSchueler, RechnungsPositionSchueler
        rechnung_sozialamt = self.model(
            sozialamt=sozialamt,
            sozialamt_anschrift=sozialamt.anschrift,
            startdatum=startdatum,
            enddatum=enddatum
        )
        rechnung_sozialamt.clean()
        rechnung_sozialamt.save()
        for schueler_in_einrichtung, tage in sozialamt.anmeldungen.get_betreuungstage(startdatum, enddatum).items():
            tage_abwesend = schueler_in_einrichtung.war_abwesend(tage)
            rechnung_schueler = RechnungSchueler.objects.erstelle_rechnung(
                rechnung_sozialamt, schueler_in_einrichtung, tage_abwesend
            )
            tage_abwesend_datetime = tage_abwesend.values_list('datum', flat=True)
            for tag in tage:
                RechnungsPositionSchueler.objects.erstelle_fuer_tag(
                    tag,
                    schueler_in_einrichtung,
                    rechnung_schueler,
                    tag in tage_abwesend_datetime
                )
            rechnung_schueler.fehltage_abrechnen(schueler_in_einrichtung)
            rechnung_schueler.abschliessen(schueler_in_einrichtung)
        return rechnung_sozialamt


class RechnungSchuelerManager(models.Manager):

    def erstelle_rechnung(self, rechnung_sozialamt, schueler_in_einrichtung, tage_abwesend):
        """
        Erstellt oder aktualisiert eine ``RechnungSchueler``-Instanz für einen Schüler.

        Der Übertrag der Fehltage erfolgt immer von der letzten vorhergehenden
        Rechnung des Schülers. Gibt es diese nicht, ist der Übertrag 0.
        """
        rechnung, created = self.update_or_create(
            rechnung_sozialamt=rechnung_sozialamt,
            schueler=schueler_in_einrichtung.schueler,
            defaults={
                'name_schueler': schueler_in_einrichtung.schueler.voller_name,
            }
        )
        if created:
            rechnung.fehltage = tage_abwesend.count()
        else:
            rechnung.fehltage = models.F('fehltage') + tage_abwesend.count()
        rechnung.save()
        rechnung.refresh_from_db()
        return rechnung


class RechnungsPositionSchuelerQuerySet(models.QuerySet):

    @staticmethod
    def get_betrachtungszeitraum(schueler_in_einrichtung, jahr):
        """
        Gibt den Beginn des Betrachtungszeitraums für das angegebene Jahr zurück.

        Beginnn ist entweder am 1.1. des angegebenen Jahres oder am Eintrittsdatum,
        wenn dieses im angegebenen Jahr liegt.
        """
        beginn = timezone.make_aware(datetime(jahr, 1, 1))
        if schueler_in_einrichtung.eintritt.year == jahr:
            beginn = schueler_in_einrichtung.eintritt
        return beginn

    def nicht_abgerechnet(self, schueler_in_einrichtung, enddatum):
        """Gibt alle nicht abgerechneten Rechnungs-Positionen zurück.

        - Ist auf den Schüler und die Einrichtung, in der dieser angemeldet ist, eingeschränkt.
        - Beginn am 1.1. des Abrechnungsjahres oder am Eintrittsdatum, wenn dieses im aktuellen Jahr liegt.
        """
        return self.filter(
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            rechnung_schueler=None,
            datum__gte=self.get_betrachtungszeitraum(schueler_in_einrichtung, enddatum.year)
        )

    def fehltage_abgerechnet(self, schueler_in_einrichtung, enddatum):
        """Gibt alle abgerechneten Rechnungs-Positionen zurück, die Fehltage sind.

        - Ist auf den Schüler und die Einrichtung, in der dieser angemeldet ist, eingeschränkt.
        - Beginn am 1.1. des Abrechnungsjahres oder am Eintrittsdatum, wenn dieses im aktuellen Jahr liegt.
        """
        return self.filter(
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            abwesend=True,
            datum__gte=self.get_betrachtungszeitraum(schueler_in_einrichtung, enddatum.year)
        ).exclude(rechnung_schueler=None)


class RechnungsPositionSchuelerManager(models.Manager):

    def erstelle_fuer_tag(self, tag, schueler_in_einrichtung, rechnung_schueler, abwesend=False):
        """
        Erstellt eine ``RechnungsPositionSchueler`` für einen Betreuungstag und einen Schüler.

        Die ``RechnungsPositionSchueler`` wird mit der passenden ``RechnungSchueler``-Instanz
        verknüpft.
        """
        rechnung_pos = self.model(
            sozialamt=schueler_in_einrichtung.schueler.sozialamt,
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            datum=tag,
            name_einrichtung=schueler_in_einrichtung.einrichtung.name,
            abwesend=abwesend,
            pflegesatz=schueler_in_einrichtung.schueler.berechne_pflegesatz(tag)
        )
        if schueler_in_einrichtung.einrichtung.hat_ferien(tag):
            rechnung_pos.tag_art = self.model.TAG_ART.ferien
        if abwesend:
            # RechnungsPositionSchueler wird als nicht abgerechneter Fehltag markiert
            rechnung_pos.fehltage_nicht_abgerechnet = rechnung_schueler
        else:
            # RechnungsPositionSchueler wird als abgerechnet markiert
            rechnung_pos.rechnung_schueler = rechnung_schueler
        rechnung_pos.clean()
        return rechnung_pos.save(force_insert=True)
