import re


def iterate_links_list(text):
    for line in text.split('\n'):
        m = re.fullmatch('# \[\[([^]]+)\]\]', line)
        if m:
            yield m.group(1)


def strip(text):
    if not text:  # для случая None
        return ''
    return text.strip()
