from django.db import models


class Schueler(models.Model):

    vorname = models.CharField("Vorname", max_length=30)
    nachname = models.CharField("Nachname", max_length=30)
    einrichtungs_art = models.ForeignKey('EinrichtungsArt', verbose_name="Einrichtung")

    class Meta:
        verbose_name = "Schüler"
        verbose_name_plural = "Schüler"
        ordering = ['nachname', 'vorname']

    def __str__(self):
        return "s.vorname s.nachname".format(s=self)


class EinrichtungsArt(models.Model):

    name = models.CharField("Name", max_length=30, unique=True)
    kuerzel = models.CharField("Kürzel", max_length=1, unique=True)

    class Meta:
        verbose_name = "Einrichtung"
        verbose_name_plural = "Einrichtungen"
        ordering = ['name']

    def __str__(self):
        return self.name


class Anwesenheit(models.Model):

    schueler = models.ForeignKey(Schueler, verbose_name="Schüler")
    einrichtungs_art = models.ForeignKey(EinrichtungsArt, verbose_name="Einrichtung")
    datum = models.DateField("Datum")
    abwesend = models.BooleanField("Abwesend", default=False)

    class Meta:
        verbose_name = "Anwesenheit"
        verbose_name_plural = "Anwesenheiten"
        ordering = ['datum', 'schueler']

    def __str__(self):
        return "{s.schueler} in {s.einrichtungs_art} am {s.datum}".format(s=self)
