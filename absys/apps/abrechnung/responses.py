import io

from datetime import date

from django.conf import settings
from django.http import HttpResponse
from django.template import Context, engines


class SaxMBSResponse(HttpResponse):

    TEMPLATE_RECHNUNG_EINRICHTUNG = '{% load abrechnung_filters %}{# 1 5 #}+0925{# 2 4 #}NEUE{# 3 6 #}ABSYS {# 4 6 #}SAXMBS{# 5 12 Dateiname#}{{ rechnungeinrichtung.rechnung_sozialamt.nummer }}.DAT {# 6 7, lückenlos aufsteigende Nummer, führende Nullen #}{{ counter|stringformat:"+07d" }}{# 7 5 Leer #}     {# 8 70 Leer #}                                                                      {# 9 3 #}H  {# 10 2 leer #}  {# 11 Haushaltsjahr, letzte zwei Ziffern #}{% now "y" %}{# 12 5 Kapitel #}{{ kapitel|stringformat:"05d" }}{# 13 2 leer #}  {# 14 5 Titel #}{{ rechnungeinrichtung.einrichtung.titel|stringformat:"05d" }}{# 15-25 89 leer #}                                                                                         {# 26 12 Buchungskennzeichen #}{{ rechnungeinrichtung.buchungskennzeichen|ljust:12 }}{# 27 12 Buchungsbetrag ohne Punkte an bei Dezimalpunkten #}{{ rechnungeinrichtung.summe|decimal_ohne_punkt|stringformat:"+012d" }}{# 28 3 Währung #}{{ waehrung }}{# 29-30 54 leer #}                                                      {# 31 8 Faelligkeit DDMMYYYY#}{{ rechnungeinrichtung.datum_faellig|date:"dmY" }}{# 32-33 23 leer #}                       {# 34 7 Zahlungspartnernummer #}{{ rechnungeinrichtung.rechnung_sozialamt.sozialamt.zahlungspartnernummer|ljust:7 }}{# 35-43 191 leer #}                                                                                                                                                                                               {# 44 1 Anord-Kz: "J" wenn BKZ, bei PK "N" #}{{ anordkz }}{# 45 1 Zahlart-Kz #}N{# 46 2 Zahlungsanzeigeschlüssel #}{{ zahlungsanzeigeschluessel|stringformat:"02i" }}{# 47 1 leer #} {# 48 2 Mahnschlüssel #}{{ mahnschluessel }}{# 49 1 Zinsschlüssel #}{{ zinsschluessel }}{# 50-60 89 leer #}                                                                                         {# 61 8 Ziffer Ebene 1 #}{{ ebene_1|ljust:8 }}{# 62 8 leer #}        {# 63 10 leer #}          {# 64 20 leer #}                    {# 65-66 62 leer #}                                                              {# 67 1 SEPA #}{{ sepa }}{# 68-69 45 leer #}                                             {# 70 35 Verwendung: Sozialamt #}{{ rechnungeinrichtung.rechnung_sozialamt.name_sozialamt|ljust:35 }}{# 71 35 Einrichtungsname #}{{ rechnungeinrichtung.name_einrichtung|ljust:35 }}{# 72 35 Datum von bis #}VOM {{ rechnungeinrichtung.rechnung_sozialamt.startdatum|date:"SHORT_DATE_FORMAT" }} BIS {{ rechnungeinrichtung.rechnung_sozialamt.enddatum|date:"SHORT_DATE_FORMAT" }}      {# 73 35 leer (kann aber Verw.Zeck sein) #}                                    '

    TEMPLATE_RECHNUNG_SCHUELER = '{% load abrechnung_filters %}{# 1 5 #}+0925{# 2 4 #}NEUE{# 3 6 #}ABSYS {# 4 6 #}SAXMBS{# 5 12 Dateiname#}{{ rechnungeinrichtung.rechnung_sozialamt.nummer }}.DAT {# 6 7, lückenlos aufsteigende Nummer, führende Nullen #}{{ counter|stringformat:"+07d" }}{# 7 5 Leer #}     {# 8 70 Leer #}                                                                      {# 9 3 #}H  {# 10 2 leer #}  {# 11 Haushaltsjahr, letzte zwei Ziffern #}{% now "y" %}{# 12 5 Kapitel #}{{ kapitel|stringformat:"05d" }}{# 13 2 leer #}  {# 14 5 Titel #}{{ rechnungeinrichtung.einrichtung.titel|stringformat:"05d" }}{# 15-25 89 leer #}                                                                                         {# 26 12 Buchungskennzeichen #}{{ einrichtungsposition.schueler.aktenzeichen|ljust:12 }}{# 27 12 Buchungsbetrag ohne Punkte an bei Dezimalpunkten #}{{ einrichtungsposition.summe|decimal_ohne_punkt|stringformat:"+012d" }}{# 28 3 Währung #}{{ waehrung }}{# 29-30 54 leer #}                                                      {# 31 8 Faelligkeit DDMMYYYY#}{{ rechnungeinrichtung.datum_faellig|date:"dmY" }}{# 32-33 23 leer #}                       {# 34 7 Zahlungspartnernummer #}{{ rechnungeinrichtung.rechnung_sozialamt.sozialamt.zahlungspartnernummer|ljust:7 }}{# 35-43 191 leer #}                                                                                                                                                                                               {# 44 1 Anord-Kz: "J" wenn BKZ, bei PK "N" #}N{# 45 1 Zahlart-Kz #}N{# 46 2 Zahlungsanzeigeschlüssel #}{{ zahlungsanzeigeschluessel|stringformat:"02i" }}{# 47 1 leer #} {# 48 2 Mahnschlüssel #}{{ mahnschluessel }}{# 49 1 Zinsschlüssel #}{{ zinsschluessel }}{# 50-60 89 leer #}                                                                                         {# 61 8 Ziffer Ebene 1 #}{{ ebene_1|ljust:8 }}{# 62 8 leer #}        {# 63 10 leer #}          {# 64 20 leer #}                    {# 65-66 62 leer #}                                                              {# 67 1 SEPA #}{{ sepa }}{# 68-69 45 leer #}                                             {# 70 35 Verwendung: Sozialamt #}{{ rechnungeinrichtung.rechnung_sozialamt.name_sozialamt|ljust:35 }}{# 71 35 Einrichtungsname #}{{ rechnungeinrichtung.name_einrichtung|ljust:35 }}{# 72 35 Datum von bis #}VOM {{ rechnungeinrichtung.rechnung_sozialamt.startdatum|date:"SHORT_DATE_FORMAT" }} BIS {{ rechnungeinrichtung.rechnung_sozialamt.enddatum|date:"SHORT_DATE_FORMAT" }}      {# 73 35 leer (kann aber Verw.Zeck sein) #}AZ: {{ einrichtungsposition.schueler.aktenzeichen|ljust:32 }}'

    TEMPLATE_SICHERUNGSDATENSATZ = '{% load abrechnung_filters %}{# 1 5 #}+0925{# 2 4 #}EEEE{# 3 6 #}ABSYS {# 4 6 #}SAXMBS{# 5 12 Dateiname#}{{ rechnungsozialamt.nummer }}.DAT {# 6 7, lückenlos aufsteigende Nummer, führende Nullen #}{{ counter|stringformat:"+07d" }}{# 7-11 82 Leer #}                                                                                  {# 12 5 Mittelwert (abgerundet) aller Kapitel #}{{ rechnungsozialamt.mittelwert_kapitel|stringformat:"05d" }}{# 13 2 leer #}  {# 14 5 Mittelwert (abgerundet) aller Titel #}{{ mittelwert_titel|stringformat:"05d" }}{# 15-26 101 leer #}                                                                                                     {# 27 12 Mittelwert Buchungsbetraege (abgerundet) mit 00 am Ende #}{{ mittelwert_summe|stringformat:"+010i" }}00{# 28-75 677 leer #}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      '

    def __init__(self, rechnung_sozialamt):
        super().__init__(content_type='text/plain', charset='iso-8859-1')
        self['Content-Disposition'] = 'attachment; filename="{0}.DAT"'.format(
            rechnung_sozialamt.nummer
        )
        self.rechnung_sozialamt = rechnung_sozialamt
        self.engine = engines['django']
        self.content = self.daten()

    def daten(self):
        with io.StringIO(newline='\r\n') as output:
            counter = 1
            summe_titel = 0
            summe_geld = 0
            for rechnung_einrichtung in self.rechnung_sozialamt.rechnungen_einrichtungen.all():
                if not rechnung_einrichtung.einrichtung.pers_bkz:
                    print(self.zeile_rechnung_einrichtung(rechnung_einrichtung, counter), file=output)
                    counter += 1
                    summe_titel = summe_titel + rechnung_einrichtung.einrichtung.titel
                    summe_geld = summe_geld + rechnung_einrichtung.summe
                else:
                    for einrichtungsposition in rechnung_einrichtung.positionen.all():
                        extra_context = {
                            'einrichtungsposition': einrichtungsposition,
                        }
                        print(
                            self.zeile_rechnung_einrichtung(rechnung_einrichtung, counter, extra_context, self.TEMPLATE_RECHNUNG_SCHUELER),
                            file=output
                        )
                        counter += 1
                        summe_titel = summe_titel + einrichtungsposition.rechnung_einrichtung.einrichtung.titel
                        summe_geld = summe_geld + einrichtungsposition.summe
            mittelwert_titel = int(summe_titel / (counter - 1))
            mittelwert_summe = int(summe_geld / (counter - 1))
            print(self.zeile_sicherungsdatensatz(counter, mittelwert_titel, mittelwert_summe), file=output)
            # Entsprechend der saxmbs Spezifikation müssen wir ein iso-8859-1 string
            # zurück geben. Es ist ferner gewünscht nicht kodierbare Zeichen
            # durch ``?`` zu ersetzen.
            # Daddurch das wir hier an dieser Stelle bereits in bytes umwandeln
            # vermeiden wir das ``make_bytes`` der Elternklasse getriggert wird
            # und wir Probleme mit dem encoding bekommen. Der Hauptgrund warum
            # wir nicht einfach ``charset=`` in ``__init__`` die ganze Arbeit
            # überlassen ist das wir so keine Möglichkeit für ``errors=replace``
            # hätten. Das wir das ``charset`` dennoch übergeben geschieht
            # ausschließlich um es expliziter zu machen.
            return output.getvalue().encode('iso-8859-1', errors='replace')

    def render_to_string(self, template, context):
        return self.engine.from_string(template).render(Context(context))
    def zeile_rechnung_einrichtung(self, rechnung_einrichtung, counter, extra_context=None, template=None):
        context = {
            'rechnungeinrichtung': rechnung_einrichtung,
            'counter': counter,
            'ebene_1': settings.ABSYS_SAX_EBENE_1,
            'kapitel': settings.ABSYS_SAX_KAPITEL,
            'mahnschluessel': settings.ABSYS_SAX_MAHNSCHLUESSEL,
            'sepa': settings.ABSYS_SAX_SEPA,
            'waehrung': settings.ABSYS_SAX_WAEHRUNG,
            'zahlungsanzeigeschluessel': settings.ABSYS_SAX_ZAHLUNGSANZEIGESCHLUESSEL,
            'zinsschluessel': settings.ABSYS_SAX_ZINSSCHLUESSEL,
            'anordkz': settings.ABSYS_SAX_ANORDKZ,
        }
        if extra_context is not None:
            context.update(extra_context)
        if template is None:
            template = self.TEMPLATE_RECHNUNG_EINRICHTUNG
        return self.render_to_string(template, context)

    def zeile_sicherungsdatensatz(self, counter, mittelwert_titel, mittelwert_summe):
        context = {
            'rechnungsozialamt': self.rechnung_sozialamt,
            'counter': counter,
            'mittelwert_titel': mittelwert_titel,
            'mittelwert_summe': mittelwert_summe,
        }
        return self.render_to_string(self.TEMPLATE_SICHERUNGSDATENSATZ, context)
