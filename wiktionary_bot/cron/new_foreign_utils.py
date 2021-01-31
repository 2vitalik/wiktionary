from os.path import join

from core.conf import conf
from libs.utils.dt import dtf
from libs.utils.io import write, read


class messages:
    data = []
    sep = '\n\n—————\n\n'
    history_filename = join(conf.data_path, 'new_foreign', 'history',
                            dtf('Ym/Ymd'))
    active_filename = join(conf.data_path, 'new_foreign', 'messages.txt')

    @classmethod
    def append(cls, message):
        cls.data.append(message)

    @classmethod
    def save(cls):
        content = cls.sep.join(cls.data)
        write(cls.history_filename, content)
        write(cls.active_filename, content)

    @classmethod
    def load(cls):
        return read(cls.active_filename).split(cls.sep)
