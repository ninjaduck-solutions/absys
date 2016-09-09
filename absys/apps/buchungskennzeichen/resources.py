from import_export import resources
from . import models


class BuchungskennzeichenResource(resources.ModelResource):

    class Meta:
        fields = ('buchungskennzeichen',)
        import_id_fields = ('buchungskennzeichen',)
        model = models.Buchungskennzeichen
