import os
from bisect import bisect_left
from shutil import copy

from libs.storage.blocks.handlers.base import BaseBlockHandler
from libs.storage.builder import ContentsStorageBuilder
from libs.storage.const import SEPARATOR
from libs.storage.error import StorageError, PageNotFound
from libs.utils.io import read, write


class ContentsBlockHandler(BaseBlockHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.index = self.titles.index(self.title)
        except ValueError:
            self.index = None

    def get_contents_and_title(self):
        block_content = read(self.path)
        if not block_content:
            raise StorageError(f'Block is empty: "{self.path}"')
        self.contents = block_content.split(SEPARATOR)
        self.titles = self.contents[0].split('\n')

    def default_empty(self, prefix):
        return f"Prefix: {prefix}"

    def get(self, silent=False):
        if self.index is None:
            if silent:
                return ''
            raise PageNotFound(f"Block doesn't contain title: '{self.title}', "
                               f"path: {self.path}")
        return self.contents[self.index]

    def do_delete(self):
        if self.index is None:
            # todo: log('Уже удалён')
            return
            # raise StorageError(f"Block doesn't contain title: '{self.title}'")
        del self.titles[self.index]
        self.contents[0] = '\n'.join(self.titles)
        del self.contents[self.index]
        self.save()
        # todo: log('Удалён')

    def do_update(self, value):
        if self.index is None:  # info: случай добавления нового элемента
            self.index = bisect_left(self.titles[1:], self.title) + 1
            self.titles.insert(self.index, self.title)
            self.contents[0] = '\n'.join(self.titles)
            self.contents.insert(self.index, value)
        else:
            if self.contents[self.index] == value:
                # todo: log('Содержимое не изменилось')
                return  # info: содержимое не изменилось
            self.contents[self.index] = value

        self.save()
        # todo: log('Сохранён')
        if len(self.titles) - 1 > self.handler.max_count:  # -1 -- это 1я строка
            self.split_block()

    def save(self):
        copy(self.path, f'{self.path}.bak')
        write(self.path, SEPARATOR.join(self.contents))
        super(ContentsBlockHandler, self).save()

    def split_block(self):
        # todo: log('Разделение файла')
        os.rename(self.path, f'{self.path}.old')
        os.mkdir(self.path)
        contents_dict = {title: content
                         for title, content in zip(self.titles[1:],
                                                   self.contents[1:])}
        SplitContentsStorageBuilder(self.handler.path, self.titles[1:],
                                    self.handler.max_count, splitting=True,
                                    contents_dict=contents_dict)
        # todo: log('Успех')


class SplitContentsStorageBuilder(ContentsStorageBuilder):
    def __init__(self, *args, contents_dict=None, **kwargs):
        self.contents_dict = contents_dict
        super().__init__(*args, **kwargs)

    def data(self, title):
        return self.contents_dict[title]
