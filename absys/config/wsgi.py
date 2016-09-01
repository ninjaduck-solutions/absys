"""
WSGI config for absys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'absys.config.settings.dev')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

if 'APACHE_PID_FILE' in os.environ and os.path.exists(os.environ['APACHE_PID_FILE']):
    import envdir
    envdir.open('/var/envdir/absys')

from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
