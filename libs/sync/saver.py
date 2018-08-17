import os
from os.path import join

from core.conf.conf import SYNC_PATH
from libs.utils.io import write, fix_path

prefixes = {
    'Викисловарь:': 'wiktionary',
    'Участник:': 'user',
    'Шаблон:': 'template',
    'Модуль:': 'module',
}


def sync_path(title):
    for prefix in prefixes:
        if title.startswith(prefix):
            new_prefix = prefixes[prefix]
            rest = title[len(prefix):]
            title = f'{new_prefix}/{rest}'
            break
    else:
        title = f'article/{title}'
    path = join(SYNC_PATH, fix_path(title))
    return f'{path}.txt'


def sync_save(title, content):
    path = sync_path(title)
    write(path, content)


def sync_delete(title):
    path = sync_path(title)
    os.remove(path)


def sync_titles(namespace):
    return []  # todo
