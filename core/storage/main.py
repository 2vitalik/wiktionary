import os
import re
from datetime import datetime, timedelta
from os.path import join, exists

from core.conf import conf
from core.storage.updaters.mixins import UpdatersValuesMixin
from libs.parse.sections.page import Page
from libs.storage.storage import Storage
from libs.utils.dt import dtp, dtf
from libs.utils.exceptions import ImpossibleError
from libs.utils.io import read, write, read_lines
from libs.utils.wikibot import get_page


class MainStorage(UpdatersValuesMixin, Storage):
    def __init__(self, lock_slug='', **kwargs):
        kwargs['path'] = conf.MAIN_STORAGE_PATH
        kwargs['tables'] = {
            'content': 'content',
            'info': 'simple',
        }
        kwargs['lock_slug'] = lock_slug
        self._articles = None
        self._articles_set = None
        self._redirects = None
        self._redirects_set = None
        super().__init__(**kwargs)

    def get(self, title, table=None, silent=False):
        if table:
            return super().get(title, table, silent)
        info = self.get(title, 'info', silent)
        content = self.get(title, 'content', silent)
        return content, info

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

    def iterate_wiki_pages(self):
        for title in self.titles:
            yield title, get_page(title)

    def iterate_pages(self, limit=None, silent=False):
        # todo: cyrilic= latin=...
        count = 0
        for title, content in self.iterate('content'):
            yield title, Page(title, content, silent=silent)
            count += 1
            if limit and count >= limit:
                break

    def iterate_daily_logs(self, slug, start_from):
        logs_path = join(self.logs_path, slug)
        curr_date = start_from.date() - timedelta(days=1)
        while curr_date <= datetime.now().date():
            curr_date += timedelta(days=1)
            path = f"{logs_path}/{dtf('Ym/Ymd', curr_date)}.txt"
            if not exists(path):
                # todo: log something?
                continue
            lines = read_lines(path)
            for line in lines:
                if not line:
                    continue
                if not re.match('\d{4}-\d\d-\d\d \d\d:\d\d:\d\d: ', line):
                    raise ImpossibleError('Wrong log format')
                log_dt = dtp(line[:19])
                if log_dt < start_from:
                    continue
                yield log_dt, line[21:]

    def latest_daily_log(self, slug):  # todo: implement also time!
        logs_path = join(self.logs_path, slug)
        latest_month = max(os.listdir(logs_path))
        latest_date = max(os.listdir(join(logs_path, latest_month)))
        return dtp(latest_date[:-4], 'Ymd')

    def latest_recent_date(self):
        return self.latest_daily_log('recent/titles')

    def iterate_recent_titles(self, start_from):
        deleted_iterator = self.iterate_daily_logs('recent/deleted', start_from)
        titles_iterator = self.iterate_daily_logs('recent/titles', start_from)
        deleted = {title for log_dt, title in deleted_iterator}
        for log_dt, title in titles_iterator:
            if title in deleted:
                continue
            yield log_dt, title

    def iterate_recent_pages(self, start_from, silent=False):
        from libs.parse.storage_page import StoragePage

        for log_dt, title in self.iterate_recent_titles(start_from):
            yield log_dt, title, StoragePage(title, silent=silent)


storage = MainStorage()
