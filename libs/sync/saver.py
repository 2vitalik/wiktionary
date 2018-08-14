from os.path import join

from core.conf.conf import SYNC_PATH
from libs.utils.io import write, fix_path

prefixes = {
    'Викисловарь:': 'wiktionary',
    'Участник:': 'user',
    'Шаблон:': 'template',
    'Модуль:': 'module',
}


def sync_save(title, content):
    for prefix in prefixes:
        if title.startswith(prefix):
            new_prefix = prefixes[prefix]
            rest = title[len(prefix):]
            title = f'{new_prefix}/{rest}'
            break
    else:
        title = f'article/{title}'
    path = join(SYNC_PATH, fix_path(title))
    write(f"{path}.txt", content)
