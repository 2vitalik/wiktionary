import os
from os.path import join, exists

from libs.storage.error import StorageError
from libs.storage.handlers import ContentStorageHandler, \
    SimpleStorageHandler
from libs.utils.dt import dt
from libs.utils.io import write, read


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
            max_count = int(read(join(table_path, '_sys', 'max_count')))
            self.handlers[table] = self.handler_types[handler_type](table_path,
                                                                    max_count)

    def __del__(self):
        if self.locked and exists(self.lock_filename):
            os.remove(self.lock_filename)

    @property
    def lock_filename(self):
        return join(self.path, 'sys', 'lock')

    def lock(self):
        if exists(self.lock_filename):
            raise StorageError(f"Can't lock: Storage is already locked: "
                               f'"{self.lock_filename}"')
        write(self.lock_filename, dt())
        self.locked = True

    def unlock(self):
        if not exists(self.lock_filename):
            raise StorageError(f"Can't unlock: Storage wan't locked: "
                               f'"{self.lock_filename}"')
        os.remove(self.lock_filename)
        self.locked = False

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
        for table, handler in self.handlers.items():
            handler.delete(title)

    def iterate(self, table):
        yield from self.handlers[table]
