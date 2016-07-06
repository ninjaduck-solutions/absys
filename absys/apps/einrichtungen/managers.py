from django.db import models


class SchuelerInEinrichtungQuerySet(models.QuerySet):

    def war_angemeldet(self, datum):
        return self.filter(
            eintritt__gte=datum,
            austritt__lte=datum
        )
