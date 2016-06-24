from django import models


class SchuelerInEinrichtungQuerySet(models.QuerySet):

    def war_angemeldet(self, datum):
        pass

    def hat_ferien(self, datum):
        pass
