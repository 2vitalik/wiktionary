import re


class TP:  # Template Pattern
    base = '{{\s*(__RE__)\s*(?:\}\}|\|)'

    lang_header = '{{-(?P<lang>[-\w]+)-(?:\|[^}]*)?\}\}'

    any_1 = \
        re.compile('({{\s*([^{|}]+)\s*[^{}]*\}\})')
    any_2 = \
        re.compile('({{\s*([^{|}]+)\s*(?:[^{}]*{{[^{}]*\}\}[^{}]*)+\}\})')
    any_3 = \
        re.compile('({{\s*([^{|}]+)\s*(?:[^{}]*{{(?:[^{}]*{{[^{}]*\}\}[^{}]*)+\}\}[^{}]*)+\}\})')


class TR:  # Template Regex
    lang_header = re.compile(TP.lang_header)


class P:
    """
    Special useful regexp patters for parsing wiktionary pages
    """
    header = '^(={__N__} *(?P<header>[^=].*?[^=]) *={__N__} *)$'


class R:
    first_header = re.compile(P.header.replace('__N__', '1'), re.MULTILINE)
    second_header = re.compile(P.header.replace('__N__', '2'), re.MULTILINE)
    third_header = re.compile(P.header.replace('__N__', '3'), re.MULTILINE)
    forth_header = re.compile(P.header.replace('__N__', '4'), re.MULTILINE)

    lang_header = re.compile(f'^(= *{TP.lang_header} *= *)$', re.MULTILINE)
