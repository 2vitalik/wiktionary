from os.path import join

from core.conf import conf
from lib.storage.storage import Storage
from lib.utils.dt import dtp, dt
from lib.utils.io import read, write


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
        return dtp(read(self.latest_edited_filename))

    @latest_edited.setter
    def latest_edited(self, value):
        write(self.latest_edited_filename, dt(value, utc=True))


if __name__ == '__main__':
    print(MainStorage().get('привет', 'content'))
