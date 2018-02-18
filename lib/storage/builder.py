import os
from os.path import join

from lib.common.io import write
from lib.common.timing import timing
from lib.storage.const import SEPARATOR
from lib.storage.structure import StructureBuilder


class BaseStorageBuilder:
    def __init__(self, path, titles):
        self.path = path
        self.titles = titles
        self.structure = StructureBuilder(titles).structure
        self.create_fs()

    @timing
    def create_fs(self):
        self.create_dir(self.path, self.structure, level=1)

    def create_dir(self, path, data, level):
        os.mkdir(path)
        for prefix, sub_data in data.items():
            # print(' ' * level, prefix)
            key = prefix
            if level > 2:
                key = str(ord(prefix[-1]))
            new_path = join(path, key)
            if type(sub_data) == dict:
                print(' ' * level, prefix)
                self.create_dir(new_path, sub_data, level + 1)
            else:
                self.save_data(new_path, prefix, sub_data)

    def save_data(self, path, prefix, titles):
        raise NotImplementedError()


class SimpleStorageBuilder(BaseStorageBuilder):
    def save_data(self, path, prefix, titles):
        lines = [f'{title}\t{self.data(title)}' for title in titles]
        write(path, '\n'.join(lines))

    def data(self, title):
        raise NotImplementedError()


class ContentsStorageBuilder(BaseStorageBuilder):
    def save_data(self, path, prefix, titles):
        titles.sort()
        titles_str = '\n'.join(titles)
        contents = [f"Prefix: {prefix}\n{titles_str}"]
        contents += [self.content(title) for title in titles]
        write(path, SEPARATOR.join(contents))

    def content(self, title):
        raise NotImplementedError()
