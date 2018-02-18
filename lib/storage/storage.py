import os
from os.path import join, exists

from lib.storage.error import StorageError
from lib.storage.handlers.content import ContentStorageHandler
from lib.storage.handlers.simple import SimpleStorageHandler
from lib.utils.dt import dt
from lib.utils.io import write


class Storage:
    handler_types = {
        'content': ContentStorageHandler,
        'simple': SimpleStorageHandler,
    }

    def __init__(self, path, tables, lock=False):
        self.path = path
        self.locked = False
        if lock:
            self.lock()
        self.handlers = {}
        for table, handler_type in tables.items():
            table_path = join(path, table)
            self.handlers[table] = self.handler_types[handler_type](table_path)

    def __del__(self):
        if self.locked:
            os.remove(self.lock_filename)

    @property
    def lock_filename(self):
        return join(self.path, 'sys', 'lock')

    def lock(self):
        if exists(self.lock_filename):
            raise StorageError(f'Storage is already locked: '
                               f'"{self.lock_filename}"')
        write(self.lock_filename, dt())
        self.locked = True

    @property
    def logs_path(self):
        return join(self.path, 'logs')

    def get(self, title, table):
        return self.handlers[table].get(title)

    def update(self, title, **kwargs):
        for table, value in kwargs.items():
            self.handlers[table].update(title, value)

    def delete(self, title):
        # log('deleted.txt', page.log())
        for table, handler in self.handlers:
            handler.delete(title)
