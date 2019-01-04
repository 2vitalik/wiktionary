import re

import requests
import time

from projects.htmls.htmls_storage import HtmlStorage
from core.storage.main import storage
from core.storage.postponed.mixins import PostponedUpdaterMixin

from libs.utils.log import log_day, log_hour, log_exception


class HtmlStorageProcessor(PostponedUpdaterMixin):
    """
    Обновление информации в хранилище `htmls`.
    """
    def __init__(self, process_all=False):
        self.process_all = process_all
        self.storage = HtmlStorage(lock_slug=self.slug())
        self.path = self.storage.path
        super().__init__()

    def run(self, limit=None):
        if self.process_all:
            iterator = storage.iterate_pages(silent=True, limit=limit)
            for i, (title, page) in enumerate(iterator):
                # print(dt(), i, title, ' -- ', end='')
                if self.process_page(page):
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
            # print('skipped.')
            return False

        # TODO: check changes?

        time.sleep(1)
        url = f'https://ru.wiktionary.org/wiki/{title}'
        html = requests.get(url).content.decode()
        html = re.sub('.*<div class="mw-parser-output">', '', html, flags=re.DOTALL)
        html = re.sub('</div><noscript>.*', '', html, flags=re.DOTALL)
        html = re.sub('<!--\s*NewPP limit report.*-->', '', html,
                      flags=re.DOTALL)
        html = html.strip()

        self.storage.update(title, html=html)
        self.log_hour('hourly_saved', title)
        self.log_day('daily_saved', title)
        # print('saved.')
        return True

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


@log_exception('htmls')
def update_recent_htmls():
    HtmlStorageProcessor().run()


@log_exception('htmls')
def update_all_htmls():
    HtmlStorageProcessor(process_all=True).run()


if __name__ == '__main__':
    update_all_htmls()
