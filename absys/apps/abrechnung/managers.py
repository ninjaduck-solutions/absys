import datetime

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from absys.apps.buchungskennzeichen.models import Buchungskennzeichen
from . import services


class RechnungSozialamtQuerySet(models.QuerySet):

    def seit(self, datum):
        """
        Gibt alle Sozialamtsrechnungen seit ``datum`` zurück.

        Das Ende des betrachteten Zeitraums ist der 31.12. im Jahr von
        ``datum``.
        """
        return self.filter(
            startdatum__gte=datum,
            enddatum__lte=datetime.date(datum.year, 12, 31)
        )


class RechnungSozialamtManager(models.Manager):

    def get_startdatum(self, sozialamt, enddatum):
        """
        Gibt das Startdatum der Rechnung für ein Sozialamt zurück.

        Existiert schon eine Rechnung für das Sozialamt, deren Enddatum im
        gleichen Jahr liegt wie das angegebene Enddatum, ist das Startdatum der
        Tag nach dem Enddatum der letzten Rechnung. Ansonsten ist es der 1.
        Januar des Jahres, das im Enddatum angegeben ist.

        ========== =========================== ==========
        Enddatum   Enddatum Rechnung-Sozialamt Startdatum
        ========== =========================== ==========
        31.05.2016 30.04.2016                  01.05.2016
        31.05.2016 30.04.2017                  01.01.2016
        31.05.2016 30.04.2015                  01.01.2016
        31.01.2016 31.12.2015                  01.01.2016
        ========== =========================== ==========

        """
        try:
            enddatum = getattr(
                self.filter(
                    sozialamt=sozialamt,
                    enddatum__year=enddatum.year
                ).order_by('-enddatum').first(), 'enddatum'
            )
        except AttributeError:
            startdatum = datetime.date(enddatum.year, 1, 1)
        else:
            startdatum = enddatum + datetime.timedelta(1)
        return startdatum

    def vorbereiten(self, sozialamt, enddatum):
        """
        Bereitet eine :model:`abrechnung.RechnungSozialamt`-Instanz vor.

        - Das Startdatum wird ermittelt
        - Ein neue Instanz wird erstellt
        - Die Daten der Instanz werden geprüft
        - Die Instanz wird nicht gespeichert

        Args:
            sozialamt (Sozialamt): :model:'schueler.Sozialamt' Instanz
            enddatum (date): Enddatum

        Returns:
            RechnungSozialamt: Eine neue
                :model:`abrechnung.RechnungSozialamt`-Instanz, die nicht
                gespeichert wurde
        """
        startdatum = self.get_startdatum(sozialamt, enddatum)
        rechnung_sozialamt = self.model(
            sozialamt=sozialamt,
            startdatum=startdatum,
            enddatum=enddatum
        )
        rechnung_sozialamt.clean()
        return rechnung_sozialamt

    @transaction.atomic
    def rechnungslauf(self, sozialamt, enddatum, bekleidungsgeld=None):
        """
        Erzeugt eine ``RechnungEinrichtung`` pro Einrichtung des Sozialamts im gewählten Zeitraum.

        1. Betreuungstage für den gewählten Zeitraum ermitteln.
        2. Abwesenheitstage pro Schüler in Einrichtung im gewählten Zeitraum
           ermitteln.
        3. Für jeden Betreuungstag im gewählten Zeitraum pro Schüler eine
           :model:`abrechnung.RechnungsPositionSchueler` erstellen und mit
           passender :model:`abrechnung.RechnungSozialamt`-Instanz verknüpfen.
        4. Noch nicht abgerechnete
           :model:`abrechnung.RechnungsPositionSchueler`-Instanzen (Fehltage)
           pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit
           erreicht.
        5. Erstellen einer :model:`abrechnung.RechnungEinrichtung`-Instanz für
           Einrichtung.
        6. :model:`abrechnung.RechnungEinrichtung`-Instanz mit Schüler
           abrechnen.
        7. Nach dem letzten Schüler wird die
           :model:`abrechnung.RechnungEinrichtung`-Instanz abgeschlossen.
        """
        from .models import RechnungEinrichtung, RechnungsPositionSchueler
        if bekleidungsgeld is None:
            bekleidungsgeld = {}
        rechnung_sozialamt = self.vorbereiten(sozialamt, enddatum)
        rechnung_sozialamt.save()
        einrichtungs_rechnungen = {}
        betreuungstage = rechnung_sozialamt.sozialamt.anmeldungen.get_betreuungstage(
            rechnung_sozialamt.startdatum,
            rechnung_sozialamt.enddatum
        )
        for schueler_in_einrichtung, tage in betreuungstage.items():
            tage_abwesend = schueler_in_einrichtung.war_abwesend(tage).values_list(
                'datum', flat=True
            )
            RechnungsPositionSchueler.objects.erstelle_fuer_tage(
                tage,
                tage_abwesend,
                schueler_in_einrichtung,
                rechnung_sozialamt
            )
            neu_abgerechnete_fehltage = rechnung_sozialamt.fehltage_abrechnen(schueler_in_einrichtung)
            rechnung_einrichtung = RechnungEinrichtung.objects.erstelle_rechnung(
                rechnung_sozialamt, schueler_in_einrichtung.einrichtung
            )
            if rechnung_einrichtung.pk not in einrichtungs_rechnungen:
                einrichtungs_rechnungen[schueler_in_einrichtung.einrichtung.pk] = rechnung_einrichtung
            rechnung_einrichtung.abrechnen(
                schueler_in_einrichtung.schueler,
                schueler_in_einrichtung.eintritt,
                tage,
                tage_abwesend,
                schueler_in_einrichtung.bargeldbetrag(
                    rechnung_sozialamt.startdatum, rechnung_sozialamt.enddatum
                ),
                bekleidungsgeld.get(schueler_in_einrichtung.pk),
                neu_abgerechnete_fehltage
            )
        for rechnung_einrichtung in einrichtungs_rechnungen.values():
            rechnung_einrichtung.abschliessen()
        return rechnung_sozialamt


class RechnungsPositionSchuelerQuerySet(models.QuerySet):

    def nicht_abgerechnet(self, schueler_in_einrichtung, enddatum):
        """Gibt alle nicht abgerechneten Rechnungs-Positionen zurück.

        - Ist auf den Schüler und die Einrichtung, in der dieser angemeldet ist, eingeschränkt.
        - Beginn am 1.1. des Abrechnungsjahres oder am Eintrittsdatum, wenn dieses im aktuellen Jahr liegt.
        """
        return self.filter(
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            abgerechnet=False,
            datum__gte=services.get_betrachtungszeitraum(
                enddatum.year, schueler_in_einrichtung.eintritt
            )
        ).order_by('datum')

    def fehltage_abgerechnet(self, schueler_in_einrichtung, enddatum):
        """Gibt alle abgerechneten Rechnungs-Positionen zurück, die Fehltage sind.

        - Ist auf den Schüler und die Einrichtung, in der dieser angemeldet ist, eingeschränkt.
        - Beginn am 1.1. des Abrechnungsjahres oder am Eintrittsdatum, wenn dieses im aktuellen Jahr liegt.
        """
        return self.filter(
            schueler=schueler_in_einrichtung.schueler,
            einrichtung=schueler_in_einrichtung.einrichtung,
            abgerechnet=True,
            abwesend=True,
            datum__gte=services.get_betrachtungszeitraum(
                enddatum.year, schueler_in_einrichtung.eintritt
            )
        )

    def summen(self):
        """Aggregiert die Summen für Fehltage, Zahltage und Aufwände."""
        return self.aggregate(
            fehltage=models.Count(
                models.Case(
                    models.When(abwesend=True, then=1),
                    output_field=models.IntegerField()
                )
            ),
            zahltage=models.Count(
                models.Case(
                    models.When(abgerechnet=True, then=1),
                    output_field=models.IntegerField()
                )
            ),
            aufwaende=models.Sum('pflegesatz')
        )


class RechnungsPositionSchuelerManager(models.Manager):

    def erstelle_fuer_tage(self, tage, tage_abwesend, schueler_in_einrichtung, rechnung_sozialamt):
        """
        Erstellt eine :model:`abrechnung.RechnungsPositionSchueler` für einen Betreuungstag und einen Schüler.

        Die :model:`abrechnung.RechnungsPositionSchueler` wird mit der
        passenden :model:`abrechnung.RechnungSozialamt`-Instanz verknüpft.
        """
        objs = []
        for tag in tage:
            obj = self.model(
                rechnung_sozialamt=rechnung_sozialamt,
                schueler=schueler_in_einrichtung.schueler,
                name_schueler=schueler_in_einrichtung.schueler.voller_name,
                einrichtung=schueler_in_einrichtung.einrichtung,
                name_einrichtung=schueler_in_einrichtung.einrichtung.name,
                datum=tag,
                abgerechnet=tag not in tage_abwesend,
                abwesend=tag in tage_abwesend,
                pflegesatz=schueler_in_einrichtung.schueler.berechne_pflegesatz(tag)
            )
            if schueler_in_einrichtung.einrichtung.hat_ferien(tag):
                obj.tag_art = self.model.TAG_ART.ferien
            objs.append(obj)
        return self.bulk_create(objs)


class RechnungsPositionEinrichtungQuerySet(models.QuerySet):

    def letzte_position(self, jahr, eintritt, sozialamt, einrichtung):
        """
        Gibt die letzte Rechnungs-Position im angegebenen Jahr zurück.

        Sozialamt und Einrichtung müssen die gleiche sein.
        """
        start = services.get_betrachtungszeitraum(jahr, eintritt)
        return self.filter(
            rechnung_einrichtung__einrichtung=einrichtung,
            rechnung_einrichtung__rechnung_sozialamt__sozialamt=sozialamt,
            rechnung_einrichtung__rechnung_sozialamt__enddatum__gte=start
        ).order_by('-rechnung_einrichtung__rechnung_sozialamt__startdatum').first()


class RechnungsPositionEinrichtungManager(models.Manager):

    def fehltage_uebertrag(self, jahr, eintritt, sozialamt, einrichtung):
        """
        Gibt die Gesamtanzahl aller Fehltage der letzten Rechnungs-Positionen im angegebenen Jahr zurück.

        Sozialamt und Einrichtung müssen die gleiche sein.

        Sollte keine Rechnung für dieses Jahr existieren, wird 0 zurückgegeben.
        """
        return getattr(self.letzte_position(jahr, eintritt, sozialamt, einrichtung), 'fehltage_gesamt', 0)


class RechnungEinrichtungManager(models.Manager):

    def erstelle_rechnung(self, rechnung_sozialamt, einrichtung):
        """
        Erstellt eine Rechnung für eine :model:`abrechnung.RechnungEinrichtung`-Instanz.

        Sollte für :model:`abrechnung.RechnungSozialamt` und
        :model:`einrichtungen.Einrichtung` schon eine Rechnung existieren wird
        diese zurückgegeben und keine neue erstellt.
        """
        def get_buchungskennzeichen():
            """
            Beziehe ein Buchungskennzeichen.

            Je nach Umgebung kann dies entweder aus dem eingespielzen BKz-Pool
            geschehen oder es kann das BKz des zugehörigen Sozialamtes verwendet werden.
            """

            if settings.ABSYS_NUTZE_SOZIALAMTS_BUCHUNGSKENNZEICHEN:
                result = rechnung_sozialamt.sozialamt.sbkz
            else:
                result = Buchungskennzeichen.objects.benutzen()
            return result

        tage_faelligkeit = datetime.timedelta(
            settings.ABSYS_TAGE_FAELLIGKEIT_EINRICHTUNG_RECHNUNG
        )
        rechnung, created = self.get_or_create(
            rechnung_sozialamt=rechnung_sozialamt,
            einrichtung=einrichtung,
            defaults={
                'datum_faellig': timezone.now().date() + tage_faelligkeit,
            }
        )
        if created:
            rechnung.betreuungstage = len(einrichtung.get_betreuungstage(
                rechnung_sozialamt.startdatum,
                rechnung_sozialamt.enddatum
            ))
            rechnung.buchungskennzeichen = get_buchungskennzeichen()
            rechnung.save()
        return rechnung
