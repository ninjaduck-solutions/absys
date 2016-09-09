from pytest_factoryboy import register

from . import factories


register(factories.RechnungSozialamtFactory)
register(factories.RechnungSchuelerFactory)
register(factories.RechnungsPositionSchuelerFactory)
