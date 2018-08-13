from os.path import join, exists

from core.conf import conf
from libs.parse.sections.page import Page
from libs.storage.storage import Storage
from libs.utils.dt import dtp, dt
from libs.utils.io import read, write


class MainStorage(Storage):
    def __init__(self, lock=False, **kwargs):
        kwargs['path'] = conf.STORAGE_PATH
        kwargs['tables'] = {
            'content': 'content',
            'info': 'simple',
        }
        kwargs['lock'] = lock
        super().__init__(**kwargs)

    @property
    def latest_edited_filename(self):
        return join(self.path, 'sys', 'latest_edited')

    @property
    def latest_edited(self):
        if not exists(self.latest_edited_filename):
            return None
        return dtp(read(self.latest_edited_filename))

    @latest_edited.setter
    def latest_edited(self, value):
        write(self.latest_edited_filename, dt(value, utc=True))

    def iterate_pages(self, limit=None, silent=False):
        # todo: cyrilic= latin=...
        count = 0
        for title, content in self.iterate('content'):
            yield title, Page(title, content, silent=silent)
            count += 1
            if limit and count >= limit:
                break


storage = MainStorage()
