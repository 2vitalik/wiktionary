import re

import requests
import time

from core.storage.postponed.storage_updater import StoragePostponedUpdaterMixin
from libs.utils.log import log_exception
from projects.htmls.htmls_storage import HtmlStorage


class HtmlStorageProcessor(StoragePostponedUpdaterMixin):
    """
    Обновление информации в хранилище `htmls`.
    """
    storage_class = HtmlStorage

    def process_page(self, page):
        title = page.title
        if title in self.storage.titles_set:
            self._debug_skipped()
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
        self._debug_processed()
        return True


@log_exception('htmls')
def update_recent_htmls():  # todo: common mechanism for such functions, e.g.: update_recent('htmls')
    HtmlStorageProcessor().run()


@log_exception('htmls')
def update_all_htmls():
    HtmlStorageProcessor(process_all=True).run()


if __name__ == '__main__':
    update_all_htmls()
