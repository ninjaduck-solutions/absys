import datetime
from import_export import resources

from . import models
from absys.apps.schueler.models import Schueler


class AnwesenheitenResource(resources.ModelResource):

    class Meta:
        model = models.Anwesenheit
        fields = ('id', 'schueler', 'schueler__nachname', 'schueler__vorname', 'datum', 'abwesend')

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        """
        Importierte Daten aufbereiten.

        Folgende Datenstruktur wird erwartet:

        ::

            Landeszentrum zur Betreuung Blinder und Sehbehinderter,Flemmingstrasse 8h,09116 Chemnitz,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
            2016.0,4.0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
            Anwesend,Text77,Bewohner,Geburtsdatum,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30
            15.0,15.0,"Apel, Anja",23.05.2001,1.0,1.0,1.0,H,H,1.0,H,H,H,1.0,H,H,1.0,1.0,1.0,1.0,1.0,H,H,1.0,1.0,1.0,1.0,1.0,H,H,H,H,H,H
            17.0,13.0,"Blume, Benjamin",17.08.2002,1.0,1.0,1.0,H,H,1.0,1.0,1.0,1.0,1.0,H,H,1.0,1.0,1.0,1.0,K,K,K,1.0,1.0,1.0,1.0,1.0,H,H,H,H,H,H
        """
        data = dataset[:]
        dataset.wipe()
        dataset.headers = ['id', 'schueler', 'schueler__nachname', 'schueler__vorname', 'datum', 'abwesend']
        year = int(data[0][0])
        month = int(data[0][1])
        days = list(map(int, data[1][4:]))
        for row in data[2:]:
            nachname, vorname = row[2].split(",", 1)
            vorname = vorname.strip()
            nachname = nachname.strip()
            schueler = Schueler.objects.get(
                vorname=vorname,
                nachname=nachname,
                geburtsdatum=datetime.datetime.strptime(row[3], '%d.%m.%Y').date()
            )
            existing_days = dict(
                schueler.anwesenheit.filter(datum__range=(
                    datetime.date(year, month, days[0]),
                    datetime.date(year, month, days[-1])
                )).values_list('datum', 'id')
            )
            for day in days:
                id = None
                datum = datetime.date(year, month, day)
                if datum in existing_days:
                    id = existing_days[datum]
                abwesend = False
                try:
                    int(row[day + 3])
                except ValueError:
                    abwesend = True
                dataset.append([id, schueler.id, schueler.nachname, schueler.vorname, datum, abwesend])
