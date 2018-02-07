from django.db import models


class SchuelerQuerySet(models.QuerySet):

    def ist_aktiv(self):
        """Liefert nur jene Schüler welche nicht explizit deaktiviert wurden."""
        return self.filter(inaktiv=False)

    def ist_inaktiv(self):
        """Liefert nur jene Schüler welche explizit deaktiviert wurden."""
        return self.filter(inaktiv=True)
