from configurations import values


class Email(object):
    """Email settings for SMTP."""

    EMAIL_HOST = values.Value('localhost')

    EMAIL_HOST_PASSWORD = values.SecretValue()

    EMAIL_HOST_USER = values.Value('noreply@example.com')

    EMAIL_PORT = values.IntegerValue(465)

    EMAIL_USE_SSL = values.BooleanValue(True)

    EMAIL_USE_TLS = values.BooleanValue(False)
