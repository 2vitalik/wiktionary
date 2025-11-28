from genericpath import exists
from os.path import join

import telegram

from core.conf import conf
from core.storage.main import storage
from core.storage.postponed.debug.debug import DebugMixin
from libs.utils.dt import dtp, dt
from libs.utils.io import read, write
from wiktionary_bot.src.slack import slack_error
from wiktionary_bot.src.utils import send


class PostponedUpdaterMixin(DebugMixin):
    path = None  # should be set in inheritor

    def process_recent_pages(self):
        for title in storage.deleted_titles(self.latest_updated):
            self.remove_page(title)

        self.new_latest_updated = self.latest_updated
        iterator = storage.iterate_changed_pages(self.latest_updated,
                                                 silent=True)
        for i, (log_dt, title, page) in enumerate(iterator):
            self._debug_title(i, title)
            self.update_page(page)
            self.new_latest_updated = log_dt
        self.latest_updated = self.new_latest_updated

    def update_page(self, page):
        raise NotImplementedError()

    def remove_page(self, title):
        raise NotImplementedError()

    @property
    def latest_updated_filename(self):
        return join(self.path, 'sys', 'latest_updated')

    @property
    def latest_updated(self):
        if not exists(self.latest_updated_filename):
            return None
        content = read(self.latest_updated_filename)
        if not content:
            msg = f'⛔ Empty file: {self.latest_updated_filename}'
            slack_error(msg)
            bot = telegram.Bot(conf.telegram_token)
            send(bot, conf.main_group_id, msg)
            raise ValueError(msg)
        return dtp(content)

    @latest_updated.setter
    def latest_updated(self, value):
        write(self.latest_updated_filename, dt(value, utc=True))
