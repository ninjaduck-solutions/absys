from django import template

register = template.Library()


@register.filter
def decimal_ohne_punkt(decimal, kommastellen=2):
    """
    Gibt einen Decimal ohne Punkt als Integer zurück.
    """
    return int(decimal.shift(kommastellen))

@register.filter
def integer_abgerundet(decimal, kommastellen=2):
    """
    Gibt einen Decimal als Integer zurück. Die Kommastellen 
    werden werden abgeschnitten.
    """
    return int(decimal)
