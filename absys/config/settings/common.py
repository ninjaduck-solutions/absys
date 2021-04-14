import os

from configurations import Configuration, values

from .values import AdminsValue


class BaseDir(object):
    """Provide absolute path to project package root directory as BASE_DIR setting.

    Use it to build your absolute paths like this::

        os.path.join(BaseDir.BASE_DIR, 'templates')
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Common(Configuration):
    """Common configuration base class."""

    SECRET_KEY = '(_j4e0=pbe(b+b1$^ch_48be0=gszglcgfzz^dy=(gnx=@m*b7'

    DEBUG = values.BooleanValue(False)

    ADMINS = AdminsValue()
    MANAGERS = ADMINS

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            'null': {
                'class': 'logging.NullHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'handlers': ['null'],
                'propagate': False,
            },
            'py.warnings': {
                'handlers': ['console'],
            },
        }
    }

    ALLOWED_HOSTS = values.ListValue(['www.example.com'])

    # Invalidate session after 120 minutes
    SESSION_COOKIE_AGE = values.IntegerValue(7200)

    SITE_ID = values.IntegerValue(1)

    # Internationalization
    # https://docs.djangoproject.com/en/dev/topics/i18n/
    LANGUAGE_CODE = values.Value('de')

    TIME_ZONE = values.Value('Europe/Berlin')

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/var/www/example.com/media/"
    MEDIA_ROOT = values.PathValue(os.path.join(BaseDir.BASE_DIR, 'media'))

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://example.com/media/", "http://media.example.com/"
    MEDIA_URL = values.Value('/media/')

    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/var/www/example.com/static/"
    STATIC_ROOT = values.PathValue(os.path.join(BaseDir.BASE_DIR, 'static_root'))

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/dev/howto/static-files/
    STATIC_URL = values.Value('/static/')

    # Additional locations of static files
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(BaseDir.BASE_DIR, 'static'),
    )

    STATICFILES_FINDERS = values.ListValue([
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    ])

    MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ]

    ROOT_URLCONF = 'absys.config.urls'

    WSGI_APPLICATION = 'absys.config.wsgi.application'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BaseDir.BASE_DIR, 'templates'), ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'absys.context_processors.django_version',
                ],
                'debug': values.BooleanValue(False,
                    environ_name='DJANGO_TEMPLATES_TEMPLATE_DEBUG'),
                # Beware before activating this! Grappelli has problems with admin
                # inlines and the template backend option 'string_if_invalid'.
                'string_if_invalid': values.Value('',
                    environ_name='DJANGO_TEMPLATES_STRING_IF_INVALID'),
            },
        },
    ]

    # the following line is only necessary because django-template-debug uses it
    TEMPLATE_DEBUG = TEMPLATES[0]['OPTIONS'].get('debug', False)

    FIXTURE_DIRS = (
        os.path.join(BaseDir.BASE_DIR, 'fixtures'),
    )

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django_filters',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',

        'crispy_forms',
        'autofixture',
        'import_export',
        'wkhtmltopdf',

        'absys.apps.abrechnung.apps.AbrechnungConfig',
        'absys.apps.anmeldung.apps.AnmeldungConfig',
        'absys.apps.anwesenheitsliste.apps.AnwesenheitslisteConfig',
        'absys.apps.einrichtungen.apps.EinrichtungenConfig',
        'absys.apps.schueler.apps.SchuelerConfig',
        'absys.apps.dashboard.apps.DashboardConfig',
        'absys.apps.buchungskennzeichen.apps.BuchungskennzeichenConfig',
        'absys.apps.benachrichtigungen.apps.BenachrichtigungenConfig',
    )

    CACHES = values. DictValue({
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    })

    CRISPY_TEMPLATE_PACK = values.Value('bootstrap3')

    WKHTMLTOPDF_CMD = values.Value('xvfb-run -- /usr/bin/wkhtmltopdf')

    EMAIL_SUBJECT_PREFIX = '[AbSys]'

    DEFAULT_FROM_EMAIL = values.EmailValue('noreply@example.com')

    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    LOGIN_URL = 'absys_login'
    LOGOUT_URL = 'absys_logout'
    LOGIN_REDIRECT_URL = 'dashboard_dashboard'

    # Custom locale formats
    FORMAT_MODULE_PATH = [
        'absys.config.locale',
    ]

    from django.contrib.messages import constants as message_constants

    MESSAGE_TAGS = {
        message_constants.DEBUG: 'debug',
        message_constants.INFO: 'info',
        message_constants.SUCCESS: 'success',
        message_constants.WARNING: 'warning',
        message_constants.ERROR: 'danger',
    }

    # Anzahl der Buchungskennzeichen die unterschritten werden muss um eine
    # 'Buchungskennzeichen gehen aus' Benachrichtigung zu veranlassen.
    ABSYS_BUCHUNGSKENNZEICHEN_MIN_VERBLEIBEND = values.IntegerValue(30)

    # Anzahl der Tage die ein Schüler noch in einer Einrichtung verbleibend ist
    # bevor eine Benachrichtigung ausgelöst wird.
    ABSYS_EINRICHTUNG_MIN_VERBLEIBENDE_TAGE = values.IntegerValue(30)

    # Anzahl der Tage für ``EinrichtungHatPflegesatz.pflegesatz_enddatum``
    # die wenn unterschritten eine Bennachrichtigung auslöst.
    ABSYS_EINRICHTUNG_HAT_PFLEGESATZ_MIN_VERBLEIBENDE_TAGE = values.IntegerValue(30)

    # Anzahl der Tage für ``Bettengeldsatz.enddatum`` die wenn unterschritten
    # eine Bennachrichtigung auslöst.
    ABSYS_BETTENGELDSATZ_MIN_VERBLEIBENDE_TAGE = values.IntegerValue(30)

    # Anzahl der Tage, die im aktuellen Monat für rückwirkende Änderungen der
    # Anwesenheitsliste im Frontend zur Verfügung stehen.
    ABSYS_ANWESENHEIT_TAGE_VORMONAT_ERLAUBT = values.IntegerValue(15)

    # Möglichkeit zur Deaktivierung der Prüfung des Datums in der
    # Anwesenheitsliste im Frontend.
    ABSYS_ANWESENHEIT_DATUMSPRUEFUNG = values.BooleanValue(True)

    # Anzahl der Tage bis zur Fälligkeit einer Rechnung einer Einrichtung
    ABSYS_TAGE_FAELLIGKEIT_EINRICHTUNG_RECHNUNG = values.IntegerValue(31)

    # Feste Adresse der Schule
    ABSYS_ADRESSE_SCHULE = values.Value(
            'Landesschule mit dem Förderschwerpunkt Hören\nFörderzentrum Samuel Heinicke\n Karl-Siegismund-Straße 2 |  04317 Leipzig'
    )

    # Ob das BKz des Sozialamtes der Sozialamtsrechcnung für alle ihre Einrichtungsrechnungen
    # verwendet werden soll.
    ABSYS_NUTZE_SOZIALAMTS_BUCHUNGSKENNZEICHEN = values.BooleanValue(False)

    # Start SaxMBS Konfiguration
    # SaxMBS Anord-Kz - "J" oder "N"
    ABSYS_SAX_ANORDKZ = values.Value('J')

    # SaxMBS Ebene 1 - String, muss acht Stellen haben
    ABSYS_SAX_EBENE_1 = values.Value('        ')

    # SaxMBS Kapitel - Integer, darf maximal fünf Stellen haben; OHNE FÜHRENDE NULLEN EINGEBEN!
    ABSYS_SAX_KAPITEL = values.IntegerValue(554)

    # SaxMBS Mahnschlüssel - Integer, darf maximal zwei Stellen haben
    ABSYS_SAX_MAHNSCHLUESSEL = values.IntegerValue(10)

    # SaxMBS SEPA - Integer, muss eine Stelle haben
    ABSYS_SAX_SEPA = values.IntegerValue(1)

    # SaxMBS Währung - String, darf maximal drei Stellen haben
    ABSYS_SAX_WAEHRUNG = values.Value('EUR')

    # SaxMBS Zahlungsanzeigeschlüssel - Integer, darf maximal zwei Stellen haben
    ABSYS_SAX_ZAHLUNGSANZEIGESCHLUESSEL = values.IntegerValue(10)

    # SaxMBS Zinsschlüssel - Integer, muss eine Stelle haben
    ABSYS_SAX_ZINSSCHLUESSEL = values.IntegerValue(1)
    # Ende SaxMBS Konfiguration
