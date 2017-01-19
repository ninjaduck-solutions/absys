from django.db import models


class BuchungskennzeichenQuerySet(models.QuerySet):

    def unerledigt(self):
        """
        Liefert alle unerledigten instanzen.

        Note:
            In der gegenwärtigen Form ist dieser Filter nur bedingt notwendig, allerdings wird er
            dennoch in Hinblick auf Konsistenz mit den anderen Benachrichtigungstypyen und zur
            leichteren Erweiterbarkeit eingeführt.
        """
        return self.filter(erledigt=False)


class SchuelerInEinrichtungLaeuftAusBenachrichtigungQuerySet(models.QuerySet):

    def unerledigt(self, schueler_in_einrichtung):
        """
        Liefert alle unerledigten Instanzen, beschränkt auf einen ``SchuelerInEinrichtung``.

        Args:
            schueler_in_einrichtung: Begrenze Benachrichtigungen auf diese Instanz.
        """
        return self.filter(schueler_in_einrichtung=schueler_in_einrichtung, erledigt=False)


class EinrichtungHatPflegesatzLaeuftAusBenachrichtigungQuerySet(models.QuerySet):

    def unerledigt(self, einrichtung_hat_pflegesatz):
        """
        Liefert alle unerledigten Benachrichtigungen für diesen ``EinrichtungHatPflegesatz``

        Args:
            einrichtung_hat_pflegesatz: Instanz für die Benachrichtigungen gefiltert werden
                sollen.
        """
        return self.filter(einrichtung_hat_pflegesatz=einrichtung_hat_pflegesatz, erledigt=False)


class BettengeldsatzLaeuftAusBenachrichtigungQuerySet(models.QuerySet):

    def unerledigt(self, bettengeldsatz):
        """
        Liefert alle unerledigten Benachrichtigungen für diesen ``Bettengeldsatz``

        Args:
            bettengeldsatz: Bettengeldsatz für die Benachrichtigungen gefiltert werden
                sollen.
        """
        return self.filter(bettengeldsatz=bettengeldsatz, erledigt=False)


class FerienBenachrichtigungQuerySet(models.QuerySet):

    def unerledigt(self, einrichtung, jahr):
        """
        Liefert für gegeb. Jahr alle unerledigten Benachrichtigungen bzgl. einer Einrichtung.

        Args:
            einrichtung: Einrichtungsinstanz der Benachrichtigung.
            jahr: Jahr auf das sich die Benachrichtigung bezieht.
        """
        return self.filter(einrichtung=einrichtung, jahr=jahr, erledigt=False)


class SchliesstageBenachrichtigungQuerySet(models.QuerySet):

    def unerledigt(self, einrichtung, jahr):
        """
        Liefert für gegeb. Jahr alle unerledigten Benachrichtigungen bzgl. einer Einrichtung.

        Args:
            einrichtung: Einrichtungsinstanz der Benachrichtigung.
            jahr: Jahr auf das sich die Benachrichtigung bezieht.
        """
        return self.filter(einrichtung=einrichtung, jahr=jahr, erledigt=False)


class BuchungskennzeichenBenachrichtigungManager(models.Manager):

    def benachrichtige(self):
        """Prüfe ob eine unerledigte Benachrichtigung vorliegt, anderfalls erstelle eine neue."""
        if not self.unerledigt():
            self.create()


class SchuelerInEinrichtungLaeuftAusBenachrichtigungManager(models.Manager):

    def benachrichtige(self, schueler_in_einrichtung):
        """
        Erstelle eine neue Benachrichtigung wenn für die genannte Instanz noch keine vorliegt.

        Args:
            schueler_in_einrichtung: Instanz auf die sich die Benachrichtigung bezieht.
        """
        if not self.unerledigt(schueler_in_einrichtung):
            return self.create(schueler_in_einrichtung=schueler_in_einrichtung)


class EinrichtungHatPflegesatzLaeuftAusBenachrichtigungManager(models.Manager):

    def benachrichtige(self, einrichtung_hat_pflegesatz):
        """
        Erstelle eine neue Benachrichtigung wenn für die genannte Instanz noch keine vorliegt.

        Args:
            einrichtung_hat_pflegesatz: Instanz auf die sich die Benachrichtigung bezieht.
        """
        if not self.unerledigt(einrichtung_hat_pflegesatz):
            return self.create(einrichtung_hat_pflegesatz=einrichtung_hat_pflegesatz)


class BettengeldsatzLaeuftAusBenachrichtigungManager(models.Manager):

    def benachrichtige(self, bettengeldsatz):
        """
        Erstelle eine neue Benachrichtigung wenn für die genannte Instanz noch keine vorliegt.

        Args:
            bettengeldsatz: Instanz auf die sich die Benachrichtigung bezieht.
        """
        if not self.unerledigt(bettengeldsatz):
            return self.create(bettengeldsatz=bettengeldsatz)


class FerienBenachrichtigungManager(models.Manager):

    def benachrichtige(self, einrichtung, jahr):
        """
        Erstelle eine neue Benachrichtigung wenn für die genannte Instanz noch keine vorliegt.

        Args:
            einrichtung: Einrichtung auf die sich die Benachrichtigung bezieht.
            jahr: Jahr auf die sich die Benachrichtigung bezieht.
        """
        if not self.unerledigt(einrichtung, jahr):
            return self.create(einrichtung=einrichtung, jahr=jahr)


class SchliesstageBenachrichtigungManager(models.Manager):

    def benachrichtige(self, einrichtung, jahr):
        """
        Erstelle eine neue Benachrichtigung wenn für die genannte Instanz noch keine vorliegt.

        Args:
            einrichtung: Einrichtung auf die sich die Benachrichtigung bezieht.
            jahr: Jahr auf die sich die Benachrichtigung bezieht.
        """
        if not self.unerledigt(einrichtung, jahr):
            return self.create(einrichtung=einrichtung, jahr=jahr)
