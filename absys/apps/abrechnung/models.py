from collections import deque, OrderedDict
import datetime
import decimal

import arrow
from django.db import models, router
from django.db.models.deletion import Collector
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from model_utils import Choices
from django.utils.functional import cached_property
from model_utils.models import TimeStampedModel

from absys.apps.einrichtungen.models import Einrichtung
from absys.apps.schueler.models import Schueler, Sozialamt

from . import managers


class RechnungSozialamt(TimeStampedModel):
    """
    Eine Sozialamtsrechnung fasst mehrere Rechnungen zusammen.

    - Sozialamt (Fremdschlüssel)
    - Sozialamt Anschrift
    - Startdatum
    - Enddatum
    """

    sozialamt = models.ForeignKey(Sozialamt, models.SET_NULL, null=True, verbose_name="Sozialamt",
        related_name='rechnungen')
    name_sozialamt = models.CharField(max_length=200)
    anschrift_sozialamt = models.TextField()
    startdatum = models.DateField("Startdatum")
    enddatum = models.DateField(
        "Enddatum",
        help_text=("Das Enddatum muss nach dem Startdatum liegen, "
            "darf aber nicht nach dem heutigen Datum liegen."
            " Außerdem müssen Startdatum und Enddatum im gleichen Jahr liegen.")
    )

    objects = managers.RechnungSozialamtManager.from_queryset(managers.RechnungSozialamtQuerySet)()

    class Meta:
        ordering = ('-startdatum', '-enddatum', 'sozialamt')
        unique_together = ('sozialamt', 'startdatum', 'enddatum')
        verbose_name = "Sozialamtsrechnung"
        verbose_name_plural = "Sozialamtsrechnungen"

    def __str__(self):
        msg = "Sozialamtsrechnung {s.nummer} für {s.sozialamt} ({s.startdatum} - {s.enddatum})"
        return msg.format(s=self)

    def save(self, *args, **kwargs):
        if self.sozialamt:
            if not self.name_sozialamt:
                self.name_sozialamt = self.sozialamt.name
            if not self.anschrift_sozialamt:
                self.anschrift_sozialamt = self.sozialamt.anschrift
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """
        Löscht diese Instanz sowie alle nachfolgenden.

        Gelöscht werden alle :model:`abrechnung.RechnungSozialamt`-Instanzen,
        die zwischen dem `startdatum` dieser Rechnung und dem 31.12. im Jahr
        von `startdatum` liegen - unabhängig vom zugehörigen Sozialamt.
        """
        using = using or router.db_for_write(self.__class__, instance=self)
        assert self._get_pk_val() is not None, (
            "%s object can't be deleted because its %s attribute is set to None." %
            (self._meta.object_name, self._meta.pk.attname)
        )
        collector = Collector(using=using)
        collector.collect(
            RechnungSozialamt.objects.seit(self.startdatum),
            keep_parents=keep_parents
        )
        return collector.delete()

    delete.alters_data = True

    def clean(self):
        if self.startdatum > self.enddatum:
            raise ValidationError(
                {'enddatum': "Das Enddatum muss nach dem Startdatum liegen."},
                code='enddatum_nach_startdatum'
            )
        if self.enddatum > now().date():
            raise ValidationError(
                {'enddatum': "Das Enddatum darf nicht nach dem heutigen Datum liegen."},
                code='enddatum_nach_heute'
            )
        if self.startdatum.year != self.enddatum.year:
            raise ValidationError(
                {'enddatum': "Startdatum und Enddatum müssen im gleichen Jahr liegen."},
                code='enddatum_und_startdatum_nicht_im_gleichen_jahr'
            )
        qs = RechnungSozialamt.objects.filter(
            models.Q(
                models.Q(startdatum__range=(self.startdatum, self.enddatum)) |
                models.Q(enddatum__range=(self.startdatum, self.enddatum))
            ) |
            models.Q(startdatum__lte=self.startdatum, enddatum__gte=self.enddatum),
            sozialamt=self.sozialamt
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.count():
            raise ValidationError(
                {'startdatum': "Für den ausgewählten Zeitraum existiert schon eine Rechnung."},
                code='startdatum_exitiert_schon'
            )
        qs = self.sozialamt.anmeldungen.zeitraum(self.startdatum, self.enddatum)
        for schueler_in_einrichtung in qs:
            einrichtung = schueler_in_einrichtung.einrichtung
            fehltage_immer_abrechnen = einrichtung.konfiguration.fehltage_immer_abrechnen
            bettengeldsaetze = einrichtung.bettengeldsaetze.zeitraum(
                self.startdatum, self.enddatum
            )
            if fehltage_immer_abrechnen and bettengeldsaetze.count() == 0:
                raise ValidationError(
                    ("Der Einrichtung {0} wurde für den Abrechnungszeitraum kein"
                        " Bettengeldsatz zugewiesen.").format(einrichtung),
                    code='einrichtung_ohne_bettengeld'
                )
            pflegesaetze = einrichtung.pflegesaetze.zeitraum(self.startdatum, self.enddatum)
            if pflegesaetze.count() == 0:
                raise ValidationError(
                    ("Der Einrichtung {0} wurde für den Abrechnungszeitraum kein"
                        " Pflegesatz zugewiesen.").format(einrichtung),
                    code='einrichtung_ohne_pflegesatz'
                )

    @property
    def nummer(self):
        return "S{:06d}".format(self.pk)

    def fehltage_abrechnen(self, schueler_in_einrichtung):
        """Nicht abgerechnete Rechnungspositionen pro Schüler seit Eintritt in die Einrichtung abrechnen."""
        qs = RechnungsPositionSchueler.objects.nicht_abgerechnet(
            schueler_in_einrichtung, self.enddatum
        )
        schueler_in_einrichtung.einrichtung.konfiguration.fehltage_abrechnen(
            qs, schueler_in_einrichtung
        )

    @cached_property
    def mittelwert_kapitel(self):
        """
        Liefere den Mittelwert aller Kapitel.

        Da jede Schule nur ein Kapitel hat, ist der Mittelwert aller Kapitel im gleich dem
        gesetzten Kapitel.
        """
        return settings.ABSYS_SAX_KAPITEL

    def get_tage(self, block_groesse=31):
        """
        Liefere eine Liste der Tage (datetime.date) im Rechnungszeitraum.

        Args:
            block_groesse (int or None, optional): Teile die Liste der Tage in
                Teilblöcke der Grösse ``block_groesse`` auf. Default ist
                ``31``.

        Returns:
            list: Eine Liste von ``deque`` Instanzen. Jedes ``deque``
            beinhaltet maximal ``block_groesse`` viele ``datetime.date``s.
            Wenn ``block_groesse=None`` oder die Anzahl der
            Tage <= ``block_groesse`` hat diese Liste nur ein Element.
        """

        tage = arrow.Arrow.range(
            'day',
            arrow.get(self.startdatum),
            arrow.get(self.enddatum)
        )
        tage = [tag.date() for tag in tage]

        result = []
        if block_groesse is None:
            result.append(tage)
        else:
            while tage:
                zeitraum = deque()
                while ((len(zeitraum) < block_groesse) and tage):
                    zeitraum.append(tage.pop(0))
                result.append(zeitraum)
        return result

    def get_prefix_tage(self, length=3):
        """Liefere eine Liste von Daten die unmittelbar vor dem Rechnungsdatum liegen."""
        start = self.startdatum - datetime.timedelta(length)
        prefix = [start + datetime.timedelta(i) for i in range(length)]
        return prefix

    def get_suffix_tage(self, length=3):
        """Liefere eine Liste von Daten die unmittelbar nach dem Rechnungsdatum liegen."""
        end = self.enddatum
        suffix = [end + datetime.timedelta(i) for i in range(1, 1 + length)]
        return suffix


class RechnungsPositionSchueler(TimeStampedModel):
    """
    Daten einer Rechnungsposition für einen Schüler an einem bestimmten Datum.

    Jede Rechnungsposition hat folgende Felder:

    - Sozialamtsrechnung (Fremdschlüssel)
    - Schüler (Fremdschlüssel)
    - Einrichtung (Fremdschlüssel)
    - Datum
    - abgerechnet
    - Name des Schülers (String)
    - Name der Einrichtung (String)
    - Schul- oder Ferientag
    - Abwesenheit
    - Verminderter Pflegesatz (Bettengeldsatz)
    - Pflegesatz

    Rechnungsposition für einen Schüler verändern ihren Zustand abhängig von
    der Anzahl der erlaubten Fehltage eines Schülers. Steigt die Anzahl der
    erlaubten Fehltage, werden ggf.auch zurückliegende Rechnungsposition eines
    Schülers abgerechnet. Dadurch ändert sich der Wert von ``abgerechnet`` und
    stimmt nicht mehr mit dem zum Zeitpunkt der Erstellung der
    Sozialamtsrechnung überein.
    """

    TAG_ART = Choices(
        ('ferien', "Ferientag"),
        ('schule', "Schultag"),
    )
    rechnung_sozialamt = models.ForeignKey(RechnungSozialamt, verbose_name="Sozialamtsrechnung",
        related_name='positionen_schueler')
    schueler = models.ForeignKey(Schueler, models.SET_NULL, null=True, verbose_name="Schüler",
        related_name='positionen_schueler')
    einrichtung = models.ForeignKey(Einrichtung, models.SET_NULL, null=True,
        verbose_name="Einrichtung", related_name='positionen_schueler')
    datum = models.DateField("Datum")
    abgerechnet = models.BooleanField("abgerechnet", default=False)
    name_schueler = models.CharField("Name des Schülers", max_length=62)
    name_einrichtung = models.CharField("Einrichtung", max_length=30)
    tag_art = models.CharField("Schul- oder Ferientag", choices=TAG_ART, default=TAG_ART.schule, max_length=20)
    abwesend = models.BooleanField("Abwesenheit", default=False)
    vermindert = models.BooleanField("Verminderter Pflegesatz (Bettengeldsatz)", default=False)
    pflegesatz = models.DecimalField("Pflegesatz", max_digits=5, decimal_places=2)

    objects = managers.RechnungsPositionSchuelerManager.from_queryset(
        managers.RechnungsPositionSchuelerQuerySet
    )()

    class Meta:
        ordering = ('rechnung_sozialamt', 'einrichtung', 'schueler', 'datum')
        unique_together = ('schueler', 'datum')
        verbose_name = "Schüler-Rechnungsposition"
        verbose_name_plural = "Schüler-Rechnungspositionen"

    def __str__(self):
        msg = (
            "Schüler-Rechnungsposition für {s.name_schueler} am {s.datum}"
            " in {s.name_einrichtung}"
        )
        return msg.format(s=self)

    def save(self, *args, **kwargs):
        if self.schueler and not self.name_schueler:
            self.name_schueler = self.schueler.voller_name
        if self.einrichtung and not self.name_einrichtung:
            self.name_einrichtung = self.einrichtung.name
        super().save(*args, **kwargs)


class RechnungEinrichtung(TimeStampedModel):
    """
    Metadaten einer Rechnung für eine Einrichtung in einem bestimmten Zeitraum.

    Pro Model-Instanz zusammen eindeutig:

    - Sozialamtsrechnung (Fremdschlüssel)
    - Einrichtung (Fremdschlüssel)

    Die folgenden Felder werden beim Erstellen oder Abschluss der Rechnung
    befüllt und können nicht mehr verändert werden. Es sind keine
    Fremdschlüssel.

    - Name der Einrichtung (Erstellung)
    - Buchungskennzeichen (Erstellung)
    - Fälligkeitsdatum (Erstellung)
    - Betreuungstage (Erstellung)
    - Rechnungssumme (Abschluss)
    """

    rechnung_sozialamt = models.ForeignKey(RechnungSozialamt, verbose_name="Sozialamtsrechnung",
        related_name='rechnungen_einrichtungen')
    einrichtung = models.ForeignKey(Einrichtung, models.SET_NULL, null=True,
        verbose_name="Einrichtung", related_name='rechnungen')
    name_einrichtung = models.CharField("Name der Einrichtung", max_length=30)
    buchungskennzeichen = models.CharField("Buchungskennzeichen", max_length=12)
    datum_faellig = models.DateField("Fälligkeitsdatum")
    betreuungstage = models.PositiveIntegerField(default=0)
    summe = models.DecimalField("Gesamtbetrag", max_digits=8, decimal_places=2, null=True)

    objects = managers.RechnungEinrichtungManager()

    class Meta:
        ordering = ('-rechnung_sozialamt__startdatum', '-rechnung_sozialamt__enddatum',
            'rechnung_sozialamt', 'einrichtung')
        unique_together = ('rechnung_sozialamt', 'einrichtung')
        verbose_name = "Einrichtungs-Rechnung"
        verbose_name_plural = "Einrichtungs-Rechnungen"

    def __str__(self):
        msg = (
            "Einrichtungs-Rechnung {s.nummer} für {s.name_einrichtung}"
            " ({s.rechnung_sozialamt.startdatum} - {s.rechnung_sozialamt.enddatum})"
        )
        return msg.format(s=self)

    def save(self, *args, **kwargs):
        if self.einrichtung and not self.name_einrichtung:
            self.name_einrichtung = self.einrichtung.name
        super().save(*args, **kwargs)

    @property
    def nummer(self):
        return "ER{:06d}".format(self.pk)

    def abrechnen(self, schueler, eintritt, tage, tage_abwesend, bargeldbetrag, bekleidungsgeld=None):
        """Erstellt für den Schüler eine Rechnungsposition.

        Die Abrechnung erfolgt für die übergebenen Anwesenheits- und
        Abwesenheitstage.
        """
        if len(tage):
            fehltage_max = self.einrichtung.anmeldungen.filter(schueler=schueler).war_angemeldet(
                tage[0]
            ).get().fehltage_erlaubt
            fehltage = len(tage_abwesend)
            fehltage_uebertrag = schueler.positionen_einrichtung.fehltage_uebertrag(
                tage[0].year, eintritt, self.rechnung_sozialamt.sozialamt, self.einrichtung
            )
            if bekleidungsgeld is None:
                bekleidungsgeld = decimal.Decimal()
            summen = schueler.positionen_schueler.filter(
                rechnung_sozialamt=self.rechnung_sozialamt,
                einrichtung=self.einrichtung,
                abgerechnet=True
            ).summen()
            return self.positionen.create(
                schueler=schueler,
                name_schueler=schueler.voller_name,
                fehltage_max=fehltage_max,
                anwesend=len(tage) - fehltage,
                fehltage=fehltage,
                fehltage_uebertrag=fehltage_uebertrag,
                fehltage_gesamt=fehltage + fehltage_uebertrag,
                fehltage_abrechnung=summen['fehltage'],
                zahltage=summen['zahltage'],
                bargeldbetrag=bargeldbetrag,
                bekleidungsgeld=bekleidungsgeld,
                summe=summen['aufwaende'] + bargeldbetrag + bekleidungsgeld
            )
        return None

    def abschliessen(self):
        """Rechnung abschließen."""
        self.summe = 0
        if self.positionen.count():
            self.summe = self.positionen.aggregate(models.Sum('summe'))['summe__sum']
        self.save()

    @cached_property
    def schliesstage(self):
        """
        Gibt alle Schliesstage einer Einrichtung im
        gewählten Zeitraum der Einrichtungsrechnung aus.
        """
        return self.einrichtung.schliesstage.filter(
            datum__range=(self.rechnung_sozialamt.startdatum,
                self.rechnung_sozialamt.enddatum)
        )

    def get_schuelerdaten(self):
        """
        Erstelle ein dict welches uns für jeden schüler die Tagespositionen liefert.

        Returns:
            dict: {Schüler: ({Tag: Schuelerposition}}
        """

        def get_tagesdaten(position):
            return {sposition.datum: sposition for sposition in position.detailabrechnung}

        return {p.schueler: get_tagesdaten(p) for p in self.positionen.all()}

    def get_prefix_tage(self, length=3):
        """Liefere eine Liste von Daten die unmittelbar vor dem Rechnungsdatum liegen."""
        return self.rechnung_sozialamt.get_prefix_tage(length)

    def get_suffix_tage(self, length=3):
        """Liefere eine Liste von Daten die unmittelbar nach dem Rechnungsdatum liegen."""
        return self.rechnung_sozialamt.get_suffix_tage(length)

    def get_prefixdaten(self, zeitraum):
        """
        Liefer ein dict der Anwesenheiten im Zeitraum für alle Schüler der Einrichtungsrechnung.

        Args:
            zeitraum (tuple): Die Prefix-Tage.

        Returns:
            dict: {Schüler: {Datum: Anwesenheit}}.
        """
        # [FIXME]
        # Statt über die die Abwesenheiten zu gehen muss hier auf evtl.
        # vorhandene Vorgängerrechnung bezug genommen werden.
        # REVIEW Hier dürfen nicht in jedem Fall die Anwesenheiten (aus
        # absys.apps.anwesenheitsliste) abgefragt werden. Die
        # Anwesenheitensdaten werden schon während des Rechnungslaufs erfasst
        # und an RechnungsPositionSchueler gespeichert. Der Grund dafür ist,
        # dass Anwesenheitensdaten im Admin geändert werden können. Die
        # Rechnungsdaten können aber nicht bearbeitet werden und bleiben so
        # konsistent. Daher dürfen in einer Rechnung nie Daten aus
        # absys.apps.anwesenheitsliste benutzt werden, wenn diese auch in
        # absys.apps.abrechnung zur Verfügung stehen. Sonst kann die
        # Darstellung inkonsistent sein, wenn die Anwesenheitensdaten
        # nachträglich verändert wurden.
        # Siehe ABSYS-9

        def get_anwesenheit(schueler, zeitraum):
            start = zeitraum[0]
            ende = zeitraum[-1]
            anwesenheiten = schueler.anwesenheit.filter(datum__gte=start, datum__lte=ende)
            return {anwesenheit.datum: anwesenheit.abwesend for anwesenheit in anwesenheiten}

        schueler = [position.schueler for position in self.positionen.all()]
        return {s: get_anwesenheit(s, zeitraum) for s in schueler}


    def get_suffixdaten(self, zeitraum):
        """
        Liefer ein dict der Anwesenheiten im Zeitraum für alle Schüler der Einrichtungsrechnung.

        Args:
            zeitraum (tuple): Die Suffix-Tage.

        Returns:
            dict: {Schüler: {Datum: Anwesenheit}}.
        """
        # REVIEW
        # - Für Randtage, die nach den abgerechneten Tagen liegen, muss die
        #   Anwesenheitsliste benutzt werden. Dies ist dann aber nur eine
        #   Prognose.
        def get_anwesenheit(schueler, zeitraum):
            start = zeitraum[0]
            ende = zeitraum[-1]
            anwesenheiten = schueler.anwesenheit.filter(datum__gte=start, datum__lte=ende)
            return {anwesenheit.datum: anwesenheit.abwesend for anwesenheit in anwesenheiten}

        schueler = [position.schueler for position in self.positionen.all()]
        return {s: get_anwesenheit(s, zeitraum) for s in schueler}

class RechnungsPositionEinrichtung(TimeStampedModel):
    """
    Daten einer Rechnungsposition für einen Schüler in einer Einrichtung in einem bestimmten Zeitraum.

    Jede Rechnungsposition hat folgende Felder:

    - Schüler (Fremdschlüssel)
    - Einrichtungs-Rechnung (Fremdschlüssel)
    - Maximale Fehltage
    - Anwesend
    - Fehltage
    - Übertrag Fehltage ab 1.1. des laufenden Jahres oder Eintritt
    - Fehltage gesamt
    - Fehltage zur Abrechnung im Abrechnungszeitraum
    - Zahltage im Abrechnungszeitraum (Anwesend + Fehltage zur Abrechnung im Abrechnungszeitraum)
    - Bargeldbetrag
    - Bekleidungsgeld
    - Summe der Aufwendungen
    """

    schueler = models.ForeignKey(
        Schueler,
        models.SET_NULL,
        null=True,
        verbose_name="Schüler",
        related_name='positionen_einrichtung')
    name_schueler = models.CharField("Name des Schülers", max_length=62)
    rechnung_einrichtung = models.ForeignKey(
        RechnungEinrichtung,
        verbose_name="Einrichtungs-Rechnung",
        related_name='positionen'
    )
    fehltage_max = models.PositiveIntegerField("Maximale Fehltage")
    anwesend = models.PositiveIntegerField("Anwesend")
    fehltage = models.PositiveIntegerField("Fehltage")
    fehltage_uebertrag = models.PositiveIntegerField(
        "Übertrag Fehltage ab 1.1. des laufenden Jahres oder Eintritt"
    )
    fehltage_gesamt = models.PositiveIntegerField("Fehltage gesamt")
    fehltage_abrechnung = models.PositiveIntegerField("Fehltage zur Abrechnung im Abrechnungszeitraum")
    zahltage = models.PositiveIntegerField("Zahltage im Abrechnungszeitraum")
    bargeldbetrag = models.DecimalField("Bargeldbetrag", max_digits=8, decimal_places=2, default=0)
    bekleidungsgeld = models.DecimalField(
        "Bekleidungsgeld", max_digits=8, decimal_places=2, default=0
    )
    summe = models.DecimalField(
        "Summe der Aufwendungen", max_digits=8, decimal_places=2, null=True
    )

    objects = managers.RechnungsPositionEinrichtungManager.from_queryset(
        managers.RechnungsPositionEinrichtungQuerySet
    )()

    class Meta:
        ordering = (
            'schueler',
            'rechnung_einrichtung',
            'rechnung_einrichtung__rechnung_sozialamt__startdatum'
        )
        unique_together = ('schueler', 'rechnung_einrichtung')
        verbose_name = "Einrichtungs-Rechnungsposition"
        verbose_name_plural = "Einrichtungs-Rechnungspositionen"

    def __str__(self):
        msg = (
            "Einrichtungs-Rechnungsposition für {s.name_schueler}"
            " in {s.rechnung_einrichtung.name_einrichtung}"
            " ({s.rechnung_einrichtung.rechnung_sozialamt.startdatum}"
            " - {s.rechnung_einrichtung.rechnung_sozialamt.enddatum})"
        )
        return msg.format(s=self)

    def save(self, *args, **kwargs):
        if self.schueler and not self.name_schueler:
            self.name_schueler = self.schueler.voller_name
        super().save(*args, **kwargs)

    @cached_property
    def detailabrechnung(self):
        """
        Gibt alle :model:`abrechnung.RechnungsPositionSchueler`-Instanzen zurück, die zu dieser Instanz gehören.
        """
        return self.schueler.positionen_schueler.filter(
            rechnung_sozialamt=self.rechnung_einrichtung.rechnung_sozialamt,
            einrichtung=self.rechnung_einrichtung.einrichtung
        )

    @cached_property
    def fehltage_anderer_zeitraum(self):
        """
        Gibt die Anzahl der in dieser EinrichtungsPosition abgerechneten Fehltage zurück,
        die nicht in den Zeitraum der Rechnung fallen.
        """
        return self.detailabrechnung.exclude(
            datum__range=(
                self.rechnung_einrichtung.rechnung_sozialamt.startdatum,
                self.rechnung_einrichtung.rechnung_sozialamt.enddatum)
        ).count()

    @cached_property
    def anwesenheitssumme(self):
        """Betrag Anwesenheit."""
        return self.detailabrechnung.filter(
            abgerechnet=True, abwesend=False
        ).aggregate(models.Sum('pflegesatz'))['pflegesatz__sum']

    @cached_property
    def abwesenheitssumme(self):
        """Betrag Abwesenheit."""
        return self.detailabrechnung.filter(
            abgerechnet=True, abwesend=True
        ).aggregate(models.Sum('pflegesatz'))['pflegesatz__sum']
