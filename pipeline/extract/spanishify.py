"""Transform Italian spelling patterns to their Spanish equivalents."""


REPLACEMENTS = [
    ('ff', 'f'),
    ('igli', 'illi'),
    ('egli', 'ej'),
    ('gn', 'n'),
    ('azio', 'acio'),
    ('uzio', 'ucio'),
    ('izio', 'icio'),
    ('vv', 'v'),
]

SUFFIX_RULES = [
    ('bile', 'ble'),
    ('attamente', 'actamente'),
    ('ale', 'al'),
    ('ele', 'el'),
    ('are', 'ar'),
    ('ere', 'er'),
    ('ire', 'ir'),
    ('ione', 'ion'),
    ('enza', 'encia'),
]


def spanishify(text):
    """Apply Italian-to-Spanish phonetic transformation rules."""
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)

    for suffix, replacement in SUFFIX_RULES:
        if text.endswith(suffix):
            text = text[:-len(suffix)] + replacement
            break  # Only apply the first matching suffix rule

    return text
