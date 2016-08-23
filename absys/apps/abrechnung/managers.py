from datetime import datetime

from django.db import models, transaction
from django.utils import timezone


class RechnungSozialamtManager(models.Manager):

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
        from .models import Rechnung, RechnungsPosition
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
            rechnung = Rechnung.objects.erstelle_rechnung(
                rechnung_sozialamt, schueler_in_einrichtung, tage_abwesend
            )
            tage_abwesend_datetime = tage_abwesend.values_list('datum', flat=True)
            for tag in tage:
                if tag in tage_abwesend_datetime:
                    RechnungsPosition.objects.erstelle_fuer_tag(tag, schueler_in_einrichtung, abwesend=True)
                else:
                    RechnungsPosition.objects.erstelle_fuer_tag(tag, schueler_in_einrichtung, rechnung)
            rechnung.fehltage_abrechnen(schueler_in_einrichtung)
            rechnung.abschliessen(schueler_in_einrichtung)
        return rechnung_sozialamt


class RechnungQuerySet(models.QuerySet):

    def letzte_rechnungen(self, jahr):
        """Gibt die letzten Rechnungen im angegebenen Jahr zurück."""
        return self.filter(
            rechnung_sozialamt__startdatum__gte=timezone.make_aware(datetime(jahr, 1, 1)),
            rechnung_sozialamt__enddatum__lte=timezone.make_aware(datetime(jahr, 12, 31))
        ).order_by('-rechnung_sozialamt__startdatum')


class RechnungManager(models.Manager):

    def erstelle_rechnung(self, rechnung_sozialamt, schueler_in_einrichtung, tage_abwesend):
        """
        Erstellt eine ``Rechnung``-Instanz für einen Schüler.

        Der Übertrag der Fehltage erfolgt immer von der letzten vorhergehenden
        Rechnung des Schülers. Gibt es diese nicht, ist der Übertrag 0.
        """
        fehltage = tage_abwesend.count()
        fehltage_uebertrag = 0
        letzte_rechnungen = schueler_in_einrichtung.schueler.rechnungen.letzte_rechnungen(
            rechnung_sozialamt.enddatum.year
        )
        if letzte_rechnungen.count():
            fehltage_uebertrag = letzte_rechnungen.first().fehltage_gesamt
        rechnung, created = self.update_or_create(
            rechnung_sozialamt=rechnung_sozialamt,
            schueler=schueler_in_einrichtung.schueler,
            defaults={
                'name_schueler': schueler_in_einrichtung.schueler.voller_name,
                'fehltage': fehltage,
                'fehltage_gesamt': (fehltage_uebertrag + fehltage),
                'max_fehltage': schueler_in_einrichtung.fehltage_erlaubt,
            }
        )
        return rechnung


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
            rechnung=None,
            datum__gte=self.get_betrachtungszeitraum(schueler_in_einrichtung, enddatum.year)
        )


class RechnungsPositionManager(models.Manager):

    def erstelle_fuer_tag(self, tag, schueler_in_einrichtung, rechnung=None, abwesend=False):
        """
        Erstellt eine ``RechnungsPosition`` für einen Betreuungstag und einen Schüler.

        Die ``RechnungsPosition`` wird mit der passenden ``Rechnung``-Instanz
        verknüpft, falls eine übergeben wurde.
        """
        kwargs = {
            'sozialamt': schueler_in_einrichtung.schueler.sozialamt,
            'schueler': schueler_in_einrichtung.schueler,
            'einrichtung': schueler_in_einrichtung.einrichtung,
            'datum': tag,
            'name_einrichtung': schueler_in_einrichtung.einrichtung.name,
            'abwesend': abwesend,
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
