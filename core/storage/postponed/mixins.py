from genericpath import exists
from os.path import join

from core.storage.main import storage
from libs.utils.dt import dtp, dt
from libs.utils.io import read, write


class PostponedUpdaterMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_latest_updated = self.latest_updated

    def process_recent_pages(self):
        pages_iterator = \
            storage.iterate_recent_pages(self.latest_updated, silent=True)
        # todo: iterate also through changed `all_pages`?..
        # todo: iterate also through `deleted` on both: `all_pages` & `recent`
        for log_dt, title, page in pages_iterator:
            self.process_page(page)
            self.new_latest_updated = log_dt
        self.latest_updated = self.new_latest_updated

    def process_page(self, page):
        raise NotImplementedError()

    @property
    def latest_updated_filename(self):
        return join(self.path, 'sys', 'latest_updated')

    @property
    def latest_updated(self):
        if not exists(self.latest_updated_filename):
            return None
        return dtp(read(self.latest_updated_filename))

    @latest_updated.setter
    def latest_updated(self, value):
        write(self.latest_updated_filename, dt(value, utc=True))
