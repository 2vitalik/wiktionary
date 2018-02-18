import os
from bisect import bisect_left

from lib.storage.const import SEPARATOR
from lib.storage.error import StorageError
from lib.storage.handlers.base import BaseStorageHandler
from lib.utils.io import read, write


class ContentStorageHandler(BaseStorageHandler):

    # todo: Использовать `cache` для ускорения массового считывания

    def get(self, title):
        path = self.block_path(title)
        return ContentsBlock(path, title).content

    def update(self, title, value):
        path = self.block_path(title)
        ContentsBlock(path, title).content = value

    def delete(self, title, value):
        path = self.block_path(title)
        # todo


class ContentsBlock:
    def __init__(self, path, title):
        self.path = path
        self.title = title
        self.contents = read(self.path).split(SEPARATOR)
        self.titles = self.contents[0].split('\n')
        try:
            self.index = self.titles.index(title)
        except ValueError:
            self.index = None

    @property
    def content(self):
        if self.index is None:
            raise StorageError(f"Block doesn't contain title: '{self.title}'")
        return self.contents[self.index]

    @content.setter
    def content(self, value):
        if self.index is None:  # info: случай добавления нового элемента
            if len(self.titles) > 1000:  # todo: self.max_count instead ?
                self.split_block()
                # todo
                return
            self.index = bisect_left(self.titles, self.title)
            self.titles.insert(self.index, self.title)
            self.contents[0] = '\n'.join(self.titles)
            self.contents.insert(self.index, value)
        else:
            self.contents[self.index] = value
        write(self.path, SEPARATOR.join(self.contents))

    def split_block(self):
        os.rename(self.path, f'{self.path}.old')
        os.mkdir(self.path)
        # todo
