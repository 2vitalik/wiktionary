import os
from os.path import isdir, isfile, join

from libs.storage.blocks.handlers.content import ContentsBlockHandler
from libs.storage.blocks.handlers.simple import SimpleBlockHandler
from libs.storage.blocks.iterators.content import ContentsBlockIterator
from libs.storage.blocks.iterators.simple import SimpleBlockIterator
from libs.utils.classes import required


class BaseStorageHandler:
    block_iterator_class = None
    block_handler_class = None

    def __init__(self, path, max_count):
        self.path = path
        self.max_count = max_count

    @required('block_iterator_class', 'block_handler_class')
    def block(self, title):
        return self.block_handler_class(title, self)

    def get(self, title):
        return self.block(title).get()

    def update(self, title, value):
        self.block(title).update(value)

    def delete(self, title):
        self.block(title).delete()

    def iterate(self, path):
        for name in os.listdir(path):
            if '.' in name:
                continue  # ignore `.bak`, `.old`, `.new`, etc.
            if name in ['_sys']:
                continue
            new_path = join(path, name)
            if isdir(new_path):
                yield from self.iterate(new_path)
            if isfile(new_path):
                yield from self.block_iterator_class(new_path)

    def __iter__(self):
        yield from self.iterate(self.path)


class ContentStorageHandler(BaseStorageHandler):
    block_iterator_class = ContentsBlockIterator
    block_handler_class = ContentsBlockHandler

    # todo: Использовать `cache` для ускорения массового считывания


class SimpleStorageHandler(BaseStorageHandler):
    block_iterator_class = SimpleBlockIterator
    block_handler_class = SimpleBlockHandler
