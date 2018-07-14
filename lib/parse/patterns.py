import re


class P(object):
    """
    Special useful regexp patters for parsing wiktionary pages
    """

    lang_header = \
        re.compile('^(= *{{-(?P<lang>[-\w]+)-(?:\|[^}]*)?\}\} *= *)$',
                   re.MULTILINE)

    second_header = \
        re.compile("^(== *(?P<value>[^=].*?[^=]) *== *)$",
                   re.MULTILINE)

    third_header = \
        re.compile("^(=== *(?P<value>[^=].*?[^=]) *=== *)$",
                   re.MULTILINE)

    forth_header = \
        re.compile("^(==== *(?P<value>[^=].*?[^=]) *==== *)$",
                   re.MULTILINE)
