from configurations import values

from . import common, databases, email, lockdown


class SSL(object):
    """Default settings for SSL-enabled servers.

    Please read Django's SSL/HTTPS documentation and modify this configuration
    as needed. Be advised that the default settings will not work with all web
    servers.
    """

    CSRF_COOKIE_SECURE = values.BooleanValue(True)

    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)

    SECURE_HSTS_SECONDS = values. IntegerValue(3600)

    SECURE_PROXY_SSL_HEADER = values.TupleValue(None)

    SECURE_REDIRECT_EXEMPT = values.ListValue([])

    SECURE_SSL_HOST = values.Value('www.example.com')

    SECURE_SSL_REDIRECT = values.BooleanValue(True)

    SESSION_COOKIE_SECURE = values.BooleanValue(True)


class Public(email.Email, databases.Databases, lockdown.Lockdown, SSL, common.Common):
    """General settings for all public servers."""

    CSRF_COOKIE_HTTPONLY = True

    SECRET_KEY = values.SecretValue()

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SILENCED_SYSTEM_CHECKS = values.ListValue([])

    X_FRAME_OPTIONS = 'DENY'


class Staging(Public):
    """Settings for staging servers."""

    pass


class Production(Public):
    """Settings for production servers."""

    pass
