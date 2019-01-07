from core.storage.main import MainStorage

from core.storage.updaters.lib.updaters.base import BaseUpdater
from libs.utils.dt import dt
from libs.utils.exceptions import ImpossibleError


class MainStorageUpdater(BaseUpdater):
    """
    Обновление информации в главном хранилище.
    """
    def __init__(self, slug):
        super().__init__(slug)
        self.storage = MainStorage(lock_slug=slug)

    def update_page(self, title, content, edited, redirect):
        edited_str = dt(edited, utc=True)
        info = f"{edited_str}, {'R' if redirect else 'A'}"
        self.storage.update(title, content=content, info=info)
        self.log_hour('changed', f'<{info}> - {title}')
        self.log_day('titles_changed', title)

    def remove_page(self, title):
        self.storage.delete(title)

    def close(self, *args, **kwargs):
        self.save_titles()
        self.storage.unlock(self.slug)

    def save_titles(self):
        titles = []
        articles = []
        redirects = []
        for title, info in self.storage.iterate('info'):
            titles.append(title)
            if info.endswith('A'):
                articles.append(title)
            elif info.endswith('R'):
                redirects.append(title)
            else:
                raise ImpossibleError()
        self.storage.save_titles(titles)
        self.storage.save_articles(articles)
        self.storage.save_redirects(redirects)
