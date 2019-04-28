import os
from os.path import join, exists

from libs.storage.error import StorageError
from libs.storage.handlers import ContentStorageHandler, \
    SimpleStorageHandler
from libs.utils.dt import dt, dtf
from libs.utils.io import write, read, write_lines, read_lines


class Storage:
    handler_types = {
        'content': ContentStorageHandler,
        'simple': SimpleStorageHandler,
    }

    def __init__(self, path, tables, max_counts=None, lock_slug=''):
        """
        Если lock_slug == '', то хранилище не блокируется
        """
        self.path = path
        self.lock_slug = lock_slug
        self.locked = False
        if lock_slug:
            self.lock(lock_slug)
        self.handlers = {}
        for table, handler_type in tables.items():
            table_path = join(path, table)
            max_count_path = join(table_path, '_sys', 'max_count')
            if exists(max_count_path):
                max_count = int(read(max_count_path))
            elif max_counts and table in max_counts:
                max_count = max_counts[table]
            else:
                raise Exception('Undefined `max_count` for storage')
            self.handlers[table] = \
                self.handler_types[handler_type](table_path, max_count)
        self._titles = None
        self._titles_set = None

    def __del__(self):
        if self.locked and self.lock_slug:
            lock_filename = self.lock_filename(self.lock_slug)
            if exists(lock_filename):
                os.remove(lock_filename)

    def lock_filename(self, lock_slug):
        return join(self.path, 'sys', f'lock_{lock_slug}')

    def lock(self, lock_slug):
        lock_filename = self.lock_filename(lock_slug)
        if exists(lock_filename):
            raise StorageError(f"Can't lock: Storage is already locked: "
                               f'"{lock_filename}"')
        write(lock_filename, dt())
        self.locked = True

    def unlock(self, lock_slug):
        lock_filename = self.lock_filename(lock_slug)
        if not exists(lock_filename):
            raise StorageError(f"Can't unlock: Storage wan't locked: "
                               f'"{lock_filename}"')
        os.remove(lock_filename)
        self.locked = False

    @property
    def titles_filename(self):
        return join(self.path, 'sys', 'titles.txt')

    def save_titles(self, titles):
        write_lines(self.titles_filename, titles)
        # path = join(self.logs_path, 'titles', f"{dtf('Ym/dts')}.txt")
        # write_lines(path, titles)

    def load_titles(self):
        return read_lines(self.titles_filename)

    @property
    def titles(self):
        if self._titles is None:
            self._titles = self.load_titles()
        return self._titles

    @property
    def titles_set(self):
        if self._titles_set is None:
            self._titles_set = set(self.titles)
        return self._titles_set

    @property
    def logs_path(self):
        return join(self.path, 'logs')

    def get(self, title, table, silent=False):
        return self.handlers[table].get(title, silent)

    def block_path(self, title, table):
        return self.handlers[table].block_path(title)

    def update(self, title, **kwargs):
        for table, value in kwargs.items():
            self.handlers[table].update(title, value)

    def delete(self, title):
        # log('deleted.txt', page.log())
        for table, handler in self.handlers.items():
            handler.delete(title)

    def iterate(self, table):
        yield from self.handlers[table]
