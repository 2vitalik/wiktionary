

def nowiki(value):
    return f'<nowiki>{value}</nowiki>'


def code(value):
    return f'<code>{value}</code>'


def nowiki_code(value):
    return code(nowiki(value))


def bold(value):
    return f"'''{value}'''"


def italic(value):
    return f"''{value}''"
