from os.path import join, exists

from core.conf import conf
from lib.parse.sections.page import Page
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
        if not exists(self.latest_edited_filename):
            return None
        return dtp(read(self.latest_edited_filename))

    @latest_edited.setter
    def latest_edited(self, value):
        write(self.latest_edited_filename, dt(value, utc=True))

    def iterate_pages(self):
        for title, content in self.iterate('content'):
            yield title, Page(title, content)


if __name__ == '__main__':
    # content = MainStorage().get('привет', 'content')
    # print(content)
    # print('=' * 100)
    #
    # content = content.replace('{{длина слова', '{{ДЛИНА СЛОВА!!')
    # MainStorage().update('привет', content=content)
    #
    # content = MainStorage().get('привет', 'content')
    # print(content)
    #
    # MainStorage().update('выпив', content='Вот так вот :)')
    # MainStorage().delete('выпив')

    # info = MainStorage().get('привет', 'info')
    # print(info)

    # MainStorage().update('привет', info='test!! :)')

    info = MainStorage().get('привет', 'info')
    print(info)

    # MainStorage().delete('привет')
