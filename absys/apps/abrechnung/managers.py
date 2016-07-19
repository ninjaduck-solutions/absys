from django.db import models
from django.db import transaction


class RechnungManager(models.Manager):

    def _erstelle_rechnung(self, sozialamt, schueler, startdatum, enddatum):
        """Erstellt eine ``Rechnung``-Instanz für einen Schüler."""
        rechnung = self.model(
            sozialamt=sozialamt,
            schueler=schueler,
            startdatum=startdatum,
            enddatum=enddatum,
            name_schueler=schueler.voller_name,
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
            rechnung = self._erstelle_rechnung(sozialamt, schueler, startdatum, enddatum)
            for schueler_in_einrichtung, tage in schueler.erstelle_einzelabrechnung(startdatum, enddatum).items():
                tage_abwesend = schueler_in_einrichtung.war_abwesend(startdatum, enddatum)
                for tag in tage:
                    if tag in tage_abwesend:
                        RechnungsPosition.erstelle_fuer_tag(tag, schueler_in_einrichtung)
                    else:
                        RechnungsPosition.erstelle_fuer_tag(tag, schueler_in_einrichtung, rechnung)
                rechnung.fehlltage_abrechnen(schueler_in_einrichtung)
                rechnung.abschliessen(schueler_in_einrichtung)


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
            create = rechnung.positionen.create
        else:
            create = self.create
        return create(**kwargs)
