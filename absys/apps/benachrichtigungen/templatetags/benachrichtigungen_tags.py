import datetime
from django import template

from absys.apps.benachrichtigungen import models

register = template.Library()

@register.simple_tag
def benachrichtigungen_string():
    # Ein link-Text zur "Benachrichtigungen" Seite welcher dynamisch die Anzahl
    # der gegenwärtig unerledigten Benachrichigungen enthält.
    count = models.Benachrichtigung.objects.filter(erledigt=False).count()
    result = 'Benachrichtigungen'
    if count:
        result += ' ({})'.format(count)
    return result
