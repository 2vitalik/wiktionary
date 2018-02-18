import os
from bisect import bisect_left
from shutil import copy

from lib.storage.builder import ContentsStorageBuilder
from lib.storage.const import SEPARATOR
from lib.storage.error import StorageError
from lib.storage.handlers.base import BaseStorageHandler
from lib.utils.io import read, write


class ContentStorageHandler(BaseStorageHandler):

    # todo: Использовать `cache` для ускорения массового считывания

    def get(self, title):
        path = self.block_path(title)
        return ContentsBlock(path, title, self).content

    def update(self, title, value):
        path = self.block_path(title)
        ContentsBlock(path, title, self).content = value

    def delete(self, title, value):
        path = self.block_path(title)
        # todo


class ContentsBlock:
    def __init__(self, path, title, handler):
        self.path = path
        self.title = title
        self.handler = handler
        block_content = read(self.path)
        if not block_content:
            raise StorageError(f'Block is empty: "{self.path}"')
        self.contents = block_content.split(SEPARATOR)
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
        copy(self.path, f'{self.path}.bak')

        if self.index is None:  # info: случай добавления нового элемента
            self.index = bisect_left(self.titles, self.title)
            self.titles.insert(self.index, self.title)
            self.contents[0] = '\n'.join(self.titles)
            self.contents.insert(self.index, value)
        else:
            self.contents[self.index] = value

        write(self.path, SEPARATOR.join(self.contents))

        if len(self.titles) > self.handler.max_count:
            self.split_block()

    def split_block(self):
        os.rename(self.path, f'{self.path}.old')
        os.mkdir(self.path)
        contents_dict = {title: content
                         for title, content in zip(self.titles[1:],
                                                   self.contents[1:])}
        SplitContentsStorageBuilder(self.handler.path, self.titles[1:],
                                    self.handler.max_count, splitting=True,
                                    contents_dict=contents_dict)


class SplitContentsStorageBuilder(ContentsStorageBuilder):
    def __init__(self, *args, contents_dict=None, **kwargs):
        self.contents_dict = contents_dict
        super(SplitContentsStorageBuilder, self).__init__(*args, **kwargs)

    def content(self, title):
        return self.contents_dict[title]
