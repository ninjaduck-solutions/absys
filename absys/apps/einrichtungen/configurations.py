import collections
import datetime


class EinrichtungKonfigurationBase:
    """
    Basis Einrichtungs-Konfiguration

    Dient ausschließlich als Basisklasse für die konkreten
    EinrichtungKonfiguration Klassen.
    """

    tage = 0
    """
    int: Anzahl der Tage.
    """

    fehltage_immer_abrechnen = False
    """
    bool: Bestimmt, ob für diese Einrichtung die Fehltage komplett abgerechnet
    werden oder nicht.

    Wenn ``False``, dann werden nur so viele Fehltage abgerechnet, wie es die
    maximalen Fehltage von :model:`einrichtungen.SchuelerInEinrichtung`
    erlaubt.

    Wenn ``True``, dann werden alle Fehltage abgerechnet, es gibt keine nicht
    abgerechneten Fehltage. Jeder Fehltag wird dann mit einem Bettengeldsatz
    abgerechnet. In diesem Fall muss vor Beginn des Rechnungslaufs geprüft
    werden, ob alle Einrichtungen mit dieser Konfiguration einen Bettengeldsatz
    haben.
    """

    bargeldauszahlung = False
    """
    bool: Bestimmt, ob Bargeldauszahlungen vorgenommen werden.

    - Bargeldauszahlungen werden auf Basis vom
      :model:`einrichtungen.Bargeldsatz` ermittelt, wo für das jeweilige
      Lebensalter ein bestimmter Betrag definiert ist
    - Das Lebensalter bezieht sich immer auf das Enddatum der Rechnung
    - Nach Erreichen des 18. Lebensjahrs wird immer der Bargeldsatz für das
      18. Lebensjahr genutzt
    - Ist kein Bargeldsatz für das Lebensalter definiert, ist der
      Bargeldsatz 0 EUR
    - Für jeden Schüler wird in :model:`einrichtungen.SchuelerInEinrichtung`
      ein Bargeldsatz-Anteil definiert (0-12), denn zur Berechnung des
      konkreten Bargeldsatz-Anteils wird folgende Formel verwendet:
      ``Bargeldsatz * Anteil / 12``
    - Da das Enddatum einer Rechnung frei definiert werden kann, muss der
      Bargeldsatz anteilig berechnet werden:
      ``Bargeldsatz-Anteil / Tage im Monat * Tage im Abrechnungszeitraum für diesen Monat``,
      danach Runden auf zwei Stellen
    """

    bekleidungsgeld = False
    """
    bool: Bestimmt, ob das Bekleidungsgeld pro Schüler in die Rechnung einfließt.

    Das Bekleidungsgeld pro Schüler in Einrichtung muss vor Erstellung der
    Sozialamtsrechnung manuell erfasst werden, wenn Bekleidungsgeld gezahlt
    wird.
    """

    feste_schliesstage = tuple()
    """
    tuple: Nummern der festen Schließtage.

    Die Nummerierung muss so erfolgen, dass sie mit
    ``datetime.date.isoweekday()`` kompatibel ist. Also Montag ist 1 und
    Sonntag ist 7.
    """

    zusammenfassungs_tabelle = False
    """
    bool: Ob in Einrichtungsrechnungen die "Zusammenfassungstabelle" dargestellt werden soll.
    """

    def fehltage_abrechnen(self, rechnungs_pos_schueler, schueler_in_einrichtung):
        """
        Methode zum Abrechnen eines Zeitraums für einen Schüler in einer Einrichtung.

        Jede Einrichtungs-Konfiguration muss diese Methode implementieren, um
        zu bestimmen welche Tage nach welchen Regeln abgerechnet werden.

        Args:
            rechnungs_pos_schueler (RechnungsPositionSchuelerQuerySet): Gesamtheit aller abzurechnenden
                Einzelpositionen. Faktisch sollten dies die nicht abgerechneten Positionen eines
                gegebenen Zeitraums sein.
            schueler_in_einrichtung (SchuelerInEinrichtung):
                Anmeldung für einen Schüler in einer Einrichtung

        Returns:
            list: Liste aller (neu) abgerechneten ``RechnungsPositionSchueler``-Instanzen.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Gibt den Namen der Einrichtungs-Konfiguration zurück.

        Returns:
            str: Name der Einrichtungs-Konfiguration
        """
        return "{.tage} Tage".format(self)


class EinrichtungKonfiguration250(EinrichtungKonfigurationBase):
    """
    Einrichtungs-Konfiguration für 250 Tage

    - Samstage und Sonntage sind feste Schließtage
    """

    tage = 250
    feste_schliesstage = (6, 7)
    zusammenfassungs_tabelle = False

    def fehltage_abrechnen(self, rechnungs_pos_schueler, schueler_in_einrichtung):
        """
        Nicht abgerechnete Rechnungspositionen pro Schüler seit Eintritt in die Einrichtung abrechnen, bis Limit erreicht.

        Note:
            Das ``limit`` ist die Anzahl der erlaubten Fehltage minus der bisher abgerechneten
            Fehltage.
        """
        limit = 0
        if len(rechnungs_pos_schueler):
            fehltage_abgerechnet = schueler_in_einrichtung.schueler.positionen_schueler.fehltage_abgerechnet(
                schueler_in_einrichtung,
                rechnungs_pos_schueler.first().rechnung_sozialamt.enddatum
            ).count()
            if fehltage_abgerechnet <= schueler_in_einrichtung.fehltage_erlaubt:
                limit = schueler_in_einrichtung.fehltage_erlaubt - fehltage_abgerechnet

        neu_abzurechnen = rechnungs_pos_schueler[:limit]
        for rechnung_pos in neu_abzurechnen:
            rechnung_pos.abgerechnet = True
            rechnung_pos.save()
        return neu_abzurechnen


class EinrichtungKonfiguration280(EinrichtungKonfigurationBase):
    """
    Einrichtungs-Konfiguration für 280 Tage

    - Samstage sind feste Schließtage
    - Bettengeldabrechnung: Fehltage x Bettengeldsatz
    """

    tage = 280
    fehltage_immer_abrechnen = True
    bargeldauszahlung = True
    bekleidungsgeld = True
    feste_schliesstage = (6,)
    zusammenfassungs_tabelle = True

    def fehltage_abrechnen(self, rechnungs_pos_schueler, schueler_in_einrichtung):
        for rechnung_pos in rechnungs_pos_schueler:
            rechnung_pos.abgerechnet = True
            rechnung_pos.pflegesatz = schueler_in_einrichtung.einrichtung.bettengeldsaetze.zeitraum(
                rechnung_pos.datum,
                rechnung_pos.datum
            ).get().satz
            rechnung_pos.save()


class EinrichtungKonfiguration365(EinrichtungKonfigurationBase):
    """
    Einrichtungs-Konfiguration für 365 Tage

    - Es gibt keine festen Schließtage
    - Ab vier oder mehr Fehltagen am Stück gilt für diese Fehltage ein
      verminderter Pflegesatz (auch Bettengeldsatz)
    - Bei der Betrachtung der Fehltage werden auch die letzten drei Tage der
      *vorhergehenden Rechnung* sowie die ersten drei *Anwesenheiten* im
      Folgezeitraum berücksichtigt
    """

    tage = 365
    fehltage_immer_abrechnen = True
    bargeldauszahlung = True
    bekleidungsgeld = True
    zusammenfassungs_tabelle = True

    def fehltage_gruppieren(self, rechnungs_pos_schueler):
        """
        Gruppen von Fehltagen zurückgeben.

        Die Fehltage werden in Gruppen aufgeteilt, die keine Lücken haben.
        """
        rechnung_pos_gruppen = []
        if len(rechnungs_pos_schueler):
            rechnung_pos_gruppen.append([rechnungs_pos_schueler[0]])
            for rechnung_pos in rechnungs_pos_schueler[1:]:
                if rechnung_pos_gruppen[-1][-1].datum == rechnung_pos.datum - datetime.timedelta(1):
                    rechnung_pos_gruppen[-1].append(rechnung_pos)
                else:
                    rechnung_pos_gruppen.append([rechnung_pos])
        return rechnung_pos_gruppen

    @staticmethod
    def fehltage_zaehlen(qs):
        """
        Anzahl der Fehltage im QuerySet zurückgeben.

        Die Fehltage müssen aufeinander folgen, damit diese gezählt werden.

        Example:
            ================== ===================
            Tage (vereinfacht) Anzhal der Fehltage
            ================== ===================
            F,F,F              3
            F,A,F              1
            A,A,A              0
            A,F,F              0
            ================== ===================
            F = fehlt
            A = anwesend
        """
        anzahl = 0
        for obj in qs:
            if obj.abwesend:
                anzahl += 1
            else:
                break
        return anzahl

    def fehltage_letzte_rechnung(self, schueler, einrichtung, startdatum):
        """Fehltage der letzten Rechnung zurückgeben."""
        return self.fehltage_zaehlen(
            schueler.positionen_schueler.filter(
                datum__lt=startdatum, einrichtung=einrichtung
            ).order_by('-datum')[:3]
        )

    def fehltage_folgezeitraum(self, schueler, enddatum):
        """Fehltage für den Folgezeitraum zurückgeben."""
        return self.fehltage_zaehlen(
            schueler.anwesenheit.filter(datum__gt=enddatum).order_by('datum')[:3]
        )

    def fehltage_abrechnen(self, rechnungs_pos_schueler, schueler_in_einrichtung):
        """
        Abrechnung der Fehltage.

        - Ab vier oder mehr Fehltagen am Stück gilt für diese Fehltage ein
          verminderter Pflegesatz (auch Bettengeldsatz)
        - Bei der Betrachtung der Fehltage werden auch die letzten drei Tage
          der *vorhergehenden Rechnung* sowie die ersten drei *Anwesenheiten*
          im Folgezeitraum berücksichtigt
        """
        for rechnung_pos_gruppe in self.fehltage_gruppieren(rechnungs_pos_schueler):
            anzahl_fehltage = len(rechnung_pos_gruppe)
            rechnung_sozialamt = rechnung_pos_gruppe[0].rechnung_sozialamt
            if rechnung_pos_gruppe[0].datum == rechnung_sozialamt.startdatum:
                anzahl_fehltage += self.fehltage_letzte_rechnung(
                    schueler_in_einrichtung.schueler,
                    schueler_in_einrichtung.einrichtung,
                    rechnung_sozialamt.startdatum
                )
            if rechnung_pos_gruppe[-1].datum == rechnung_sozialamt.enddatum:
                anzahl_fehltage += self.fehltage_folgezeitraum(
                    schueler_in_einrichtung.schueler, rechnung_sozialamt.enddatum
                )
            for rechnung_pos in rechnung_pos_gruppe:
                rechnung_pos.abgerechnet = True
                if bool(anzahl_fehltage >= 4):
                    rechnung_pos.vermindert = True
                    rechnung_pos.pflegesatz = schueler_in_einrichtung.einrichtung.bettengeldsaetze.zeitraum(
                        rechnung_pos.datum,
                        rechnung_pos.datum
                    ).get().satz
                rechnung_pos.save()


registry_classes = (
    EinrichtungKonfiguration250,
    EinrichtungKonfiguration280,
    EinrichtungKonfiguration365,
)

registry = collections.OrderedDict([(klass.tage, klass()) for klass in registry_classes])

choices = tuple([(obj_id, str(obj)) for obj_id, obj in registry.items()])
