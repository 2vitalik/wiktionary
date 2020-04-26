from collections import defaultdict
from os.path import join

from core.conf import conf
from core.storage.main import storage
from libs.utils.io import write


def update_langs():
    lists = defaultdict(list)
    for title, page in storage.iterate_pages(silent=True):
        for lang in page.languages.keys:
            lists[lang].append(title)
    path = join(conf.PARSED_STORAGE_PATH, 'lists', 'langs')
    for lang, titles in lists.items():
        write(f'{path}/{lang or "-"}.txt', '\n'.join(titles))


if __name__ == '__main__':
    update_langs()
