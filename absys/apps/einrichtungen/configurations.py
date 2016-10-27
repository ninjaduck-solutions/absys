class EinrichtungsKonfigurationBase:
    """
    Basis EinrichtungsKonfiguration

    Dient ausschließlich als Basisklasse für die konkreten
    EinrichtungsKonfiguration Klassen.
    """

    fehltage_immer_abrechnen = None
    """
    Bestimmt, ob für diese Einrichtung die Fehltage komplett abgerechnet werden
    oder nicht.

    ``True``: Alle Fehltage werden abgerechnet, es gibt keine nicht
    abgerechneten Fehltage
    """

    feste_schliesstage = tuple()
    """
    Tuple mit den Nummern der festen Schließtage.

    Die Nummerierung muss so erfolgen, dass sie mit
    ``datetime.date.isoweekday()`` kompatibel ist. Also Montag ist 1 und
    Sonntag ist 7.
    """

    def abrechnen(self, rechnung_einrichtung, schueler, eintritt, tage, tage_abwesend):
        """
        Methode zum Abrechnen eines Zeitraums für einen Schüler in einer Einrichtung.

        Jede EinrichtungsKonfiguration muss diese Methode implementieren, um
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
        Gibt den Namen der EinrichtungsKonfiguration zurück.

        Muss von jeder EinrichtungsKonfiguration implementiert werden.

        Returns:
            str: Name der EinrichtungsKonfiguration
        """
        raise NotImplementedError


class EinrichtungsKonfiguration250(EinrichtungsKonfigurationBase):

    fehltage_immer_abrechnen = False
    feste_schliesstage = (6, 7)

    def abrechnen(self, schueler, eintritt, tage, tage_abwesend):
        pass

    def __str__(self):
        return "250 Tage"


class EinrichtungsKonfiguration280(EinrichtungsKonfigurationBase):

    fehltage_immer_abrechnen = True
    feste_schliesstage = (6,)

    def abrechnen(self, schueler, eintritt, tage, tage_abwesend):
        pass

    def __str__(self):
        return "280 Tage"


class EinrichtungsKonfiguration365(EinrichtungsKonfigurationBase):

    fehltage_immer_abrechnen = True

    def abrechnen(self, schueler, eintritt, tage, tage_abwesend):
        pass

    def __str__(self):
        return "365 Tage"
