import collections


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
      konkreten Bargeldsatzes wird folgende Formel verwendet:
      ``Bargeldsatz * Anteil / 12``
    - Da das Enddatum einer Rechnung frei definiert werden kann, muss der
      Bargeldsatz anteilig berechnet werden:
      ``Bargeldsatz / Tage im Monat * Tage im Abrechnungszeitraum für diesen Monat``,
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

    def abrechnen(self, rechnung_einrichtung, schueler, eintritt, tage, tage_abwesend):
        """
        Methode zum Abrechnen eines Zeitraums für einen Schüler in einer Einrichtung.

        Jede Einrichtungs-Konfiguration muss diese Methode implementieren, um
        zu bestimmen welche Tage abgerechnet werden.

        Args:
            rechnung_einrichtung (RechnungEinrichtung): Rechnung für eine Einrichtung
            schueler (Schueler): Schüler Instanz
            eintritt (date): Tag des Eintritts in die Einrichtung
            tage (tuple): Tupel von date Objekten, die den Zeitraum zur
                Abrechnung bestimmen
            tage_abwesend (QuerySet): Liste von date Objekten, die die abwesenden
                Tage definiert

        Returns:
            QuerySet: Ein QuerySet von RechnungsPositionEinrichtung Instanzen
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

    def abrechnen(self, rechnung_einrichtung, schueler, eintritt, tage, tage_abwesend):
        pass


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

    def abrechnen(self, rechnung_einrichtung, schueler, eintritt, tage, tage_abwesend):
        pass


class EinrichtungKonfiguration365(EinrichtungKonfigurationBase):
    """
    Einrichtungs-Konfiguration für 365 Tage

    - Es gibt keine festen Schließtage
    - Ab vier oder mehr Fehltagen am Stück gilt für alle Fehltage ein
      verminderter Bettengeldsatz

        - Es gibt hier also zwei Bettengeldsätze: Standard und vermindert
    """

    tage = 365
    fehltage_immer_abrechnen = True
    bargeldauszahlung = True
    bekleidungsgeld = True

    def abrechnen(self, rechnung_einrichtung, schueler, eintritt, tage, tage_abwesend):
        pass


registry_classes = (
    EinrichtungKonfiguration250,
    EinrichtungKonfiguration280,
    EinrichtungKonfiguration365,
)

registry = collections.OrderedDict([(klass.tage, klass()) for klass in registry_classes])

choices = tuple([(obj_id, str(obj)) for obj_id, obj in registry.items()])
