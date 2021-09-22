from collections import defaultdict
from os.path import join

from core.conf import conf
from core.storage.main import storage
from libs.utils.io import write


def update_langs():
    all_articles = defaultdict(list)
    without_redirects = defaultdict(list)
    # for title, page in storage.iterate_pages_with_info(silent=True):
    for title, page in storage.iterate_pages(silent=True):
        for lang in page.languages.keys:
            all_articles[lang].append(title)
            # if not page.is_redirect:
            if title not in storage.redirects_set:
                without_redirects[lang].append(title)

    path = join(conf.PARSED_STORAGE_PATH, 'lists', 'langs')
    for lang, titles in all_articles.items():
        write(f'{path}/{lang or "-"}.txt', '\n'.join(titles))

    path = join(conf.PARSED_STORAGE_PATH, 'lists', 'langs', 'articles')
    for lang, titles in without_redirects.items():
        write(f'{path}/{lang or "-"}.txt', '\n'.join(titles))


if __name__ == '__main__':
    update_langs()
