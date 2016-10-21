import io

from django.http import HttpResponse
from django.template import Context, engines, loader


class SaxMBSResponse(HttpResponse):

    def __init__(self, rechnung_sozialamt):
        super().__init__(content_type='text/plain')
        self['Content-Disposition'] = 'attachment; filename="{0}.DAT"'.format(
            rechnung_sozialamt.nummer
        )
        self.rechnung_sozialamt = rechnung_sozialamt
        self.content = self.daten()

    def daten(self):
        with io.StringIO(newline='\r\n') as output:
            counter = 0
            for rechnung_einrichtung in self.rechnung_sozialamt.rechnungen_einrichtungen.all():
                print(self.zeile_rechnung_einrichtung(rechnung_einrichtung, counter), file=output)
                counter += 1
            print(self.zeile_sicherungsdatensatz(), file=output)
            return output.getvalue()

    def zeile_rechnung_einrichtung(self, rechnung_einrichtung, counter):
        context = {
            'rechnungeinrichtung': rechnung_einrichtung,
            'counter': counter,
        }
        return loader.render_to_string('saxmbs/rechnung_einrichtung.dat', context)

    def zeile_sicherungsdatensatz(self):
        context = {
            'rechnungsozialamt': self.rechnung_sozialamt,
        }
        return loader.render_to_string('saxmbs/sicherungsdatensatz.dat', context)
