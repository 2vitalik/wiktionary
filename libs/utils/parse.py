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


def remove_stress(value):
    return value.replace('́', '').replace('̀', '').replace('ѐ', 'е'). \
        replace('ѝ', 'и')


def find_comments(value):
    return re.findall('<!--.*?-->', value, flags=re.DOTALL)


def remove_comments(value):
    return re.sub('<!--.*?-->', '', value, flags=re.DOTALL)
