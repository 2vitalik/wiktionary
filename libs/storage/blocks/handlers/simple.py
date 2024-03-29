import os
from bisect import bisect_left
from os.path import exists
from shutil import copy

from libs.storage.blocks.handlers.base import BaseBlockHandler
from libs.storage.builder import SimpleStorageBuilder
from libs.storage.error import StorageError
from libs.utils.io import read, write


class SimpleBlockHandler(BaseBlockHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.index = self.titles.index(self.title)
        except ValueError:
            self.index = None

    def get_contents_and_title(self):
        block_content = read(self.path)
        if block_content:
            self.contents = block_content.split('\n')
        else:
            # это тоже может быть, например, когда в файлы была единственная
            # статья, котороая потом была удалена
            self.contents = []
        self.titles = [line.split('\t')[0] for line in self.contents]

    def default_empty(self, prefix):
        return ''

    def get(self, silent=False):
        if self.index is None:
            if silent:
                return ''
            raise StorageError(f"Block doesn't contain title: '{self.title}', "
                               f"path: {self.path}")
        return self.contents[self.index].split('\t', maxsplit=1)[1]

    def do_delete(self):
        if self.index is None:
            # todo: log('Уже удалён')
            return
            # raise StorageError(f"Block doesn't contain title: '{self.title}'")
        del self.titles[self.index]
        del self.contents[self.index]
        self.save()

    def do_update(self, value):
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
        super(SimpleBlockHandler, self).save()

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
