import re

from core.storage.authors import AuthorsStorage
from core.storage.main import storage
from core.storage.postponed.mixins import PostponedUpdaterMixin

from libs.utils.dt import dt
from libs.utils.log import log_day, log_hour, log_exception
from libs.utils.wikibot import get_page


class AuthorsStorageProcessor(PostponedUpdaterMixin):
    """
    Обновление информации в хранилище `authors`.
    """
    def __init__(self, process_all=False):
        self.process_all = process_all
        self.storage = AuthorsStorage(lock_slug=self.slug())
        self.path = self.storage.path
        super().__init__()

    def run(self, limit=None):
        if self.process_all:
            iterator = storage.iterate_pages(silent=True, limit=limit)
            for i, (title, page) in enumerate(iterator):
                # print(dt(), i, title, ' -- ', end='')
                self.process_page(page)
                if not i % 100:
                    self.save_titles()
                    # print(dt(), '## Titles saved!')
        else:
            self.process_recent_pages()
        self.close()

    def remove_page(self, title):
        self.storage.delete(title)

    def process_page(self, page):
        title = page.title
        if title in self.storage.titles_set:
            # Информация об авторе этой статьи уже сохранена
            # print('skipped.')
            return

        # get oldest revision
        oldest = next(get_page(title).revisions(reverseOrder=True, total=1,
                                                content=True))

        created_at = dt(oldest.timestamp, utc=True)
        created_lang = self.get_created_lang(title, oldest.text)
        created_author = oldest.user

        created = f"{created_at}, {created_lang}, {created_author}"
        # print(created)

        self.storage.update(title, created=created)
        self.log_hour('saved', f'<{created}> - {title}')
        self.log_day('titles_saved', title)

    def get_created_lang(self, title, text):
        if text is None:
            return '??'

        rules = {
            '{{-([-\w]+|Праславянский)-(?:\|[^}]+)?\}\}':
                1,
            '^= *Праславянский':
                'Праславянский',
            '=<div style="background-color0?:#{{h1c\}\}">Эсперанто</div>=':
                'eo',
            '{{заголовок\|(en|tr|jbo|la|it|es|fo|da|de|pt|hr|pl|fi|lv|nl|sv|'
            'no|io|gd|az|ms|id|nv|nds|nah|hu|nrm|vls|fur|ga|lb|hsb|li|tpi|gv|'
            'fr|cy|fy|sc|zu|sw|mg|oc|ca|qu|ln|eo|so|cs|uz|et|vo|ku|su|sk|mi|'
            'kw|bar|br|an|sq|bs|af)\|add=\w*\}\}':
                1,
            '== *\[\[?(:w)?:en:[^|]+\|английский\]\]? *== *\n':
                'en',
            '== *\[\[?(:w)?:de:[^|]+\|немецкий\]\]? *== *\n':
                'de',
            '== *\[?\[?(английский|english)\]?\]? *== *\n':
                'en',
            '== *\[?\[?(французский)\]?\]? *== *\n':
                'fr',
            '== *\[?\[?(италь?янский)\]?\]? *== *\n':
                'it',
            '== *\[?\[?(Нидерландский)\]?\]? *== *\n':
                'nl',
            '{{(английский|en)\}\}':
                'en',
            '{{(Нидерландский|nl)\}\}':
                'nl',
            '{{(немецкий|de)\}\}':
                'de',
            '{{(it)\}\}':
                'it',
            '{{NEW\|lang=([-a-z]+)\|cat=':
                1,
            '#(redirect|перенаправление)':
                '-',
        }
        for pattern, result in rules.items():
            m = re.search(pattern, text,
                          flags=re.MULTILINE | re.UNICODE | re.IGNORECASE)
            if m:
                if result == 1:
                    return m.group(1)
                return result

        self.log_day('unknown_lang', title)  # todo: save text?
        return '?'

    @property
    def logs_path(self):
        return self.storage.logs_path

    def slug(self):
        return 'all' if self.process_all else 'recent'

    def log_day(self, sub_slug, value):
        log_day(f"{self.slug()}/{sub_slug}", value, path=self.logs_path)

    def log_hour(self, sub_slug, value):
        log_hour(f"{self.slug()}/{sub_slug}", value, path=self.logs_path)

    def close(self, *args, **kwargs):
        self.save_titles()
        self.storage.unlock(self.slug())

    def save_titles(self):
        titles = []
        for title, info in self.storage.iterate('created'):
            titles.append(title)
        self.storage.save_titles(titles)


@log_exception('authors')
def update_recent_authors():
    AuthorsStorageProcessor().run()


if __name__ == '__main__':
    update_recent_authors()

    # AuthorsStorageProcessor().run()
    # AuthorsStorageProcessor().close()
    # AuthorsStorageProcessor(process_all=True).run()
