from configurations import values


class Lockdown(object):
    """Lock down the entire site."""

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ('lockdown',)

    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + ['lockdown.middleware.LockdownMiddleware']

    LOCKDOWN_ENABLED = values.BooleanValue(False)

    LOCKDOWN_PASSWORDS = values.TupleValue()

    LOCKDOWN_URL_EXCEPTIONS = values.TupleValue()

    LOCKDOWN_AUTHFORM_STAFF_ONLY = values.BooleanValue(False)

    LOCKDOWN_AUTHFORM_SUPERUSERS_ONLY = values.BooleanValue(False)
