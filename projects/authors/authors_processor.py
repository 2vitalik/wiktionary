import re

from core.storage.postponed.storage_updater import StoragePostponedUpdaterMixin
from libs.utils.dt import dt
from libs.utils.log import log_exception
from libs.utils.wikibot import get_page
from projects.authors.authors_storage import AuthorsStorage


class AuthorsStorageProcessor(StoragePostponedUpdaterMixin):
    """
    Обновление информации в хранилище `authors`.
    """
    storage_class = AuthorsStorage

    def process_page(self, page):  # todo: rename to `update_page`
        title = page.title
        if title in self.storage.titles_set:
            # Информация об авторе этой статьи уже сохранена
            self._debug_skipped()
            return False

        # get oldest revision
        oldest = next(get_page(title).revisions(reverseOrder=True, total=1,
                                                content=True))
        created_at = dt(oldest.timestamp, utc=True)
        created_lang = self.get_created_lang(title, oldest.text)
        created_author = oldest.user
        created = f"{created_at}, {created_lang}, {created_author}"
        self._debug_info(created)

        self.storage.update(title, created=created)
        self.log_hour('saved', f'<{created}> - {title}')
        self.log_day('titles_saved', title)
        self._debug_processed()
        return True

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


@log_exception('authors')
def update_recent_authors():
    AuthorsStorageProcessor().run()


@log_exception('authors')
def update_all_authors():
    AuthorsStorageProcessor(process_all=True).run()


if __name__ == '__main__':
    update_recent_authors()
