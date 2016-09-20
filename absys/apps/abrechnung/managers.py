from datetime import datetime, timedelta

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from absys.apps.buchungskennzeichen.models import Buchungskennzeichen


class RechnungSozialamtManager(models.Manager):

    @transaction.atomic
    def rechnungslauf(self, sozialamt, startdatum, enddatum):
        """
        Erzeugt eine ``RechnungEinrichtung`` pro Einrichtung des Sozialamts im gewählten Zeitraum.

        1. Abwesenheitstage pro Schüler im gewählten Zeitraum ermitteln.
        2. Für jeden Betreuungstag im gewählten Zeitraum pro Schüler eine ``RechnungsPositionSchueler`` erstellen und mit passender ``RechnungSozialamt``-Instanz verknüpfen.
        3. Noch nicht abgerechnete ``RechnungsPositionSchueler``-Instanzen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.
        4. Erstellen einer ``RechnungEinrichtung``-Instanz für Einrichtung.
        5. ``RechnungEinrichtung``-Instanz mit Schüler abrechnen.
        6. ``RechnungEinrichtung``-Instanz abschließen.
        """
        from .models import RechnungEinrichtung, RechnungsPositionSchueler
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
            tage_abwesend_datetime = tage_abwesend.values_list('datum', flat=True)
            for tag in tage:
                RechnungsPositionSchueler.objects.erstelle_fuer_tag(
                    tag,
                    schueler_in_einrichtung,
                    rechnung_sozialamt,
                    tag in tage_abwesend_datetime
                )
            rechnung_sozialamt.fehltage_abrechnen(schueler_in_einrichtung)
            rechnung_einrichtung = RechnungEinrichtung.objects.erstelle_rechnung(
                rechnung_sozialamt, schueler_in_einrichtung.einrichtung
            )
            rechnung_einrichtung.abrechnen(schueler_in_einrichtung.schueler)
            rechnung_einrichtung.abschliessen()
        return rechnung_sozialamt


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
            abgerechnet=False,
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
        ).exclude(abgerechnet=False)


class RechnungsPositionSchuelerManager(models.Manager):

    def erstelle_fuer_tag(self, tag, schueler_in_einrichtung, rechnung_sozialamt, abwesend=False):
        """
        Erstellt eine ``RechnungsPositionSchueler`` für einen Betreuungstag und einen Schüler.

        Die ``RechnungsPositionSchueler`` wird mit der passenden ``RechnungSozialamt``-Instanz
        verknüpft.
        """
        rechnung_pos = self.model(
            rechnung_sozialamt=rechnung_sozialamt,
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            datum=tag,
            abgerechnet=not abwesend,
            name_schueler=schueler_in_einrichtung.schueler.voller_name,
            name_einrichtung=schueler_in_einrichtung.einrichtung.name,
            abwesend=abwesend,
            pflegesatz=schueler_in_einrichtung.schueler.berechne_pflegesatz(tag)
        )
        if schueler_in_einrichtung.einrichtung.hat_ferien(tag):
            rechnung_pos.tag_art = self.model.TAG_ART.ferien
        return rechnung_pos.save(force_insert=True)


class RechnungEinrichtungManager(models.Manager):

    def erstelle_rechnung(self, rechnung_sozialamt, einrichtung):
        """
        Erstellt eine Rechnung für eine :model:`RechnungEinrichtung`-Instanz.

        Sollte für :model:`RechnungSozialamt` und :model:`Einrichtung` schon
        eine Rechnung existieren wird diese zurückgegeben und keine neue
        erstellt.
        """
        tage_faelligkeit = timedelta(
            settings.ABSYS_TAGE_FAELLIGKEIT_EINRICHTUNG_RECHNUNG
        )
        rechnung, created = self.get_or_create(
            rechnung_sozialamt=rechnung_sozialamt,
            einrichtung=einrichtung,
            defaults={
                'name_einrichtung': einrichtung.name,
                'datum_faellig': timezone.now().date() + tage_faelligkeit,
            }
        )
        if created:
            rechnung.betreuungstage = len(einrichtung.get_betreuungstage(
                rechnung_sozialamt.startdatum,
                rechnung_sozialamt.enddatum
            ))
            rechnung.buchungskennzeichen = Buchungskennzeichen.objects.benutzen()
            rechnung.save()
        return rechnung
