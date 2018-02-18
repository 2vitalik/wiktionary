from bisect import bisect_left
from shutil import copy

import os

from lib.storage.builder import SimpleStorageBuilder
from lib.storage.error import StorageError
from lib.utils.io import read, write


class SimpleBlock:
    def __init__(self, path, title, handler):
        self.path = path
        self.title = title
        self.handler = handler
        block_content = read(self.path)
        if not block_content:
            raise StorageError(f'Block is empty: "{self.path}"')
        self.contents = block_content.split('\n')
        self.titles = [line.split('\t')[0] for line in self.contents]
        try:
            self.index = self.titles.index(title)
        except ValueError:
            self.index = None

    def get(self):
        if self.index is None:
            raise StorageError(f"Block doesn't contain title: '{self.title}'")
        return self.contents[self.index].split('\t', maxsplit=1)[1]

    def delete(self):
        if self.index is None:
            raise StorageError(f"Block doesn't contain title: '{self.title}'")
        del self.titles[self.index]
        del self.contents[self.index]
        self.save()

    def update(self, value):
        new_value = f"{self.title}\t{value}"
        if self.index is None:  # info: случай добавления нового элемента
            self.index = bisect_left(self.titles, self.title)
            self.titles.insert(self.index, self.title)
            self.contents.insert(self.index, new_value)
        else:
            self.contents[self.index] = new_value

        self.save()
        if len(self.titles) > self.handler.max_count:
            self.split_block()

    def save(self):
        copy(self.path, f'{self.path}.bak')
        write(self.path, '\n'.join(self.contents))

    def get_data_dict(self):
        data_dict = {}
        for line in self.contents:
            title, data = line.split('\t', maxsplit=1)
            data_dict[title] = data
        return data_dict

    def split_block(self):
        os.rename(self.path, f'{self.path}.old')
        os.mkdir(self.path)
        SplitSimpleStorageBuilder(self.handler.path, self.titles,
                                  self.handler.max_count, splitting=True,
                                  data_dict=self.get_data_dict())


class SplitSimpleStorageBuilder(SimpleStorageBuilder):
    def __init__(self, *args, data_dict=None, **kwargs):
        self.data_dict = data_dict
        super().__init__(*args, **kwargs)

    def data(self, title):
        return self.data_dict[title]
