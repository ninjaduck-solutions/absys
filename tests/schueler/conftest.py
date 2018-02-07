from .factories import GruppeFactory, SchuelerFactory, SozialamtFactory


from pytest_factoryboy import register

register(SchuelerFactory)
register(SozialamtFactory)
register(GruppeFactory)
