# -*- encoding: utf-8 -*-

# The *_INPUT_FORMATS strings use the Python strftime format syntax,
# see http://docs.python.org/library/datetime.html#strftime-strptime-behavior
DATE_INPUT_FORMATS = [
    '%d.%m.%Y', '%d.%m.%y',     # '25.10.2006', '25.10.06'
    '%d%m%y',  # '251006'
]
