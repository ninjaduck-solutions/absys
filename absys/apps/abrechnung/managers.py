from datetime import datetime

from django.db import models, transaction
from django.utils import timezone


class RechnungManager(models.Manager):

    def _erstelle_rechnung(self, schueler_in_einrichtung, startdatum, enddatum):
        """Erstellt eine ``Rechnung``-Instanz für einen Schüler."""
        fehltage = schueler_in_einrichtung.war_abwesend(startdatum, enddatum)
        rechnung = self.model(
            sozialamt=schueler_in_einrichtung.sozialamt,
            schueler=schueler_in_einrichtung.schueler,
            startdatum=startdatum,
            enddatum=enddatum,
            name_schueler=schueler_in_einrichtung.schueler.voller_name,
            fehltage=fehltage,
            fehltage_gesamt=(
                schueler_in_einrichtung.schueler.rechnungen.letzte_rechnung_fehltage_gesamt(enddatum.year) +
                fehltage
            ),
            max_fehltage=schueler_in_einrichtung.fehltage_erlaubt,
        )
        rechnung.full_clean()
        rechnung.save()
        return rechnung

    @transaction.atomic
    def rechnungslauf(self, sozialamt, startdatum, enddatum):
        """
        Erzeugt eine ``Rechnung`` pro Schüler des Sozialamts im gewählten Zeitraum.

        1. Erstellen einer ``Rechnung``-Instanz pro Schüler.
        2. Abwesenheitstage pro Schüler im gewählten Zeitraum ermitteln.
        3. Für jeden Betreuungstag im gewählten Zeitraum pro Schüler eine ``RechnungsPosition`` erstellen und wenn nötig mit passender ``Rechnung``-Instanz verknüpfen.
        4. Noch nicht abgerechnete ``RechnungsPosition``-Instanzen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.
        5. ``Rechnung``-Instanz pro Schüler aktualisieren (Summe und Fehltage).
        """
        from .models import RechnungsPosition
        for schueler in sozialamt.schueler.all():
            for schueler_in_einrichtung, tage in schueler.angemeldet_in_einrichtung.get_betreuungstage(startdatum, enddatum).items():
                rechnung = self._erstelle_rechnung(schueler_in_einrichtung, startdatum, enddatum)
                tage_abwesend = schueler_in_einrichtung.war_abwesend(startdatum, enddatum)
                for tag in tage:
                    if tag in tage_abwesend:
                        RechnungsPosition.objects.erstelle_fuer_tag(tag, schueler_in_einrichtung)
                    else:
                        RechnungsPosition.objects.erstelle_fuer_tag(tag, schueler_in_einrichtung, rechnung)
                rechnung.fehltage_abrechnen(schueler_in_einrichtung)
                rechnung.abschliessen(schueler_in_einrichtung)

    def letzte_rechnung(self, jahr):
        """Gibt die letzte Rechnung im angegebenen Jahr zurück."""
        jahr_beginn = timezone.make_aware(datetime(jahr, 1, 1))
        return self.filter(startdatum__gte=jahr_beginn).order_by('-startdatum').first()

    def letzte_rechnung_fehltage_gesamt(self, jahr):
        """
        Gibt die Gesamtanzahl aller Fehltage der letzten Rechnung im angegebenen Jahr zurück.

        Sollte keine Rechnung für dieses Jahr existieren, wird 0 zurückgegeben.
        """
        return getattr(self.letzte_rechnung(jahr), 'fehltage_gesamt', 0)


class RechnungsPositionQuerySet(models.QuerySet):

    @staticmethod
    def get_betrachtungszeitraum(schueler_in_einrichtung, jahr):
        """
        Gibt den Beginn des Betrachtungszeitraums für das angegebene Jahr zurück.

        Beginnn ist entweder am 1.1. des angegebenen Jahres oder am Eintrittsdatum,
        wenn dieses im angegebenen Jahr liegt.
        """
        beginn = timezone.make_aware(datetime(jahr, 1, 1))
        if schueler_in_einrichtung.eintritt.year == jahr:
            beginn = schueler_in_einrichtung.einrichtung.eintritt
        return beginn

    def nicht_abgerechnet(self, schueler_in_einrichtung, enddatum):
        """Gibt alle nicht abgerechneten Rechnungs-Positionen zurück.

        - Ist auf den Schüler und die Einrichtung, in der dieser angemeldet ist, eingeschränkt.
        - Beginn am 1.1. des Abrechnungsjahres oder am Eintrittsdatum, wenn dieses im aktuellen Jahr liegt.
        """
        return self.filter(
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            rechnung=None,
            datum__gte=self.get_betrachtungszeitraum(schueler_in_einrichtung, enddatum.year)
        )


class RechnungsPositionManager(models.Manager):

    def erstelle_fuer_tag(self, tag, schueler_in_einrichtung, rechnung=None):
        """
        Erstellt eine ``RechnungsPosition`` für einen Betreuungstag und einen Schüler.

        Die ``RechnungsPosition`` wird mit der passenden ``Rechnung``-Instanz
        verknüpft, falls eine übergeben wurde.
        """
        kwargs = {
            'sozialamt': schueler_in_einrichtung.schueler.sozialamt,
            'schueler': schueler_in_einrichtung.schueler,
            'einrichtung': schueler_in_einrichtung.einrichtung,
            'name_einrichtung': schueler_in_einrichtung.einrichtung.name,
            'datum': tag,
            'pflegesatz': schueler_in_einrichtung.schueler.berechne_pflegesatz(tag),
        }
        if schueler_in_einrichtung.einrichtung.hat_ferien(tag):
            kwargs['tag_art'] = self.model.TAG_ART.ferien
        if rechnung:
            # Nutzt die create() Methode der Relation zwischen Rechnung und
            # RechnungsPosition
            create = rechnung.positionen.create
        else:
            # Nutzt die create() Methode von RechnungsPosition, dadurch wird
            # keine Rechnung zugewiesen
            create = self.create
        return create(**kwargs)
