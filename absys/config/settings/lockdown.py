from configurations import values


class Lockdown(object):
    """Lock down the entire site."""

    @property
    def INSTALLED_APPS(self):
        return super(Lockdown, self).INSTALLED_APPS + ('lockdown',)

    @property
    def MIDDLEWARE_CLASSES(self):
        return super(Lockdown, self).MIDDLEWARE_CLASSES + (
            'lockdown.middleware.LockdownMiddleware',
        )

    LOCKDOWN_ENABLED = values.BooleanValue(False)

    LOCKDOWN_PASSWORDS = values.TupleValue()

    LOCKDOWN_URL_EXCEPTIONS = values.TupleValue()

    LOCKDOWN_AUTHFORM_STAFF_ONLY = values.BooleanValue(False)

    LOCKDOWN_AUTHFORM_SUPERUSERS_ONLY = values.BooleanValue(False)
