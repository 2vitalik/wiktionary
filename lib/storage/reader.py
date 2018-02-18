import os
from bisect import bisect_left
from os.path import join, exists, isfile

from core.conf import conf
from lib.common.io import read, write
from lib.common.unicode import char_info
from lib.storage.const import MAX_DEPTH, SEPARATOR


class StorageError(Exception):
    pass


def block_path(title):
    path = conf.STORAGE_PATH
    category, name = char_info(title[0])

    candidates = [
        join(path, category),
        join(path, category, name),
    ]

    path = candidates[-1]
    for i in range(min(len(title), MAX_DEPTH)):
        key = str(ord(title[i]))  # код соответствующего символа
        path = join(path, key)
        candidates.append(path)

    for candidate in candidates:
        if not exists(candidate):
            raise StorageError(f"Path does't exist: '{candidate}'")
        if isfile(candidate):
            return candidate

    raise StorageError(f"Path does't exist for title '{title}'")


class Block:
    cache = {}  # todo: Использовать `cache` для ускорения массового считывания
    cached = []
    cache_size = 400

    def __init__(self, title):
        self.title = title
        self.path = block_path(title)
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
            if len(self.titles) > 1000:
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


if __name__ == '__main__':
    print(Block('привет').content)
