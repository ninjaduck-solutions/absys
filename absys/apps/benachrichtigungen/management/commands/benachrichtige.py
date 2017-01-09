from django.core.management.base import BaseCommand

from absys.apps.benachrichtigungen import services


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        prüfungen = (
            services.pruefe_schueler_in_einrichtung,
            services.pruefe_einrichtung_hat_pflegesatz,
            services.pruefe_bettengeldsatz,
            services.pruefe_ferien,
            services.pruefe_schliesstage
        )
        for prüfung in prüfungen:
            prüfung()


