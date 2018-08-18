from os.path import join, exists

from core.conf import conf
from core.storage.updaters.mixins import UpdatersValuesMixin
from libs.parse.sections.page import Page
from libs.storage.storage import Storage
from libs.utils.dt import dtp, dt
from libs.utils.io import read, write


class MainStorage(UpdatersValuesMixin, Storage):
    def __init__(self, lock=False, **kwargs):
        kwargs['path'] = conf.MAIN_STORAGE_PATH
        kwargs['tables'] = {
            'content': 'content',
            'info': 'simple',
        }
        kwargs['lock'] = lock
        self._articles = None
        self._articles_set = None
        self._redirects = None
        self._redirects_set = None
        super().__init__(**kwargs)

    @property
    def articles_filename(self):
        return join(self.path, 'sys', 'articles.txt')

    def save_articles(self, articles):
        write(self.articles_filename, '\n'.join(articles))

    def load_articles(self):
        return read(self.articles_filename).split('\n')

    @property
    def articles(self):
        if self._articles is None:
            self._articles = self.load_articles()
        return self._articles

    @property
    def articles_set(self):
        if self._articles_set is None:
            self._articles_set = set(self.articles)
        return self._articles_set

    @property
    def redirects_filename(self):
        return join(self.path, 'sys', 'redirects.txt')

    def save_redirects(self, redirects):
        write(self.redirects_filename, '\n'.join(redirects))

    def load_redirects(self):
        return read(self.redirects_filename).split('\n')

    @property
    def redirects(self):
        if self._redirects is None:
            self._redirects = self.load_redirects()
        return self._redirects
    
    @property
    def redirects_set(self):
        if self._redirects_set is None:
            self._redirects_set = set(self.redirects)
        return self._redirects_set

    def iterate_pages(self, limit=None, silent=False):
        # todo: cyrilic= latin=...
        count = 0
        for title, content in self.iterate('content'):
            yield title, Page(title, content, silent=silent)
            count += 1
            if limit and count >= limit:
                break


storage = MainStorage()
