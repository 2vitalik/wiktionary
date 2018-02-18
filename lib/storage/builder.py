import os
from os.path import join, exists
from shutil import copy

from lib.storage.error import StorageError
from lib.utils.io import write
from lib.utils.timing import timing
from lib.storage.const import SEPARATOR
from lib.storage.structure import StructureBuilder


class BaseStorageBuilder:
    def __init__(self, path, titles, max_count=1000, splitting=False):
        self.path = path
        self.titles = titles
        self.max_count = max_count
        self.splitting = splitting
        self.structure = StructureBuilder(titles, max_count).structure
        self.create_fs()

    @timing
    def create_fs(self):
        self.create_dir(self.path, self.structure, level=1)
        write(join(self.path, '_sys', 'max_count'), str(self.max_count))

    def create_dir(self, path, structure, level):
        if not self.splitting or not exists(path):
            os.mkdir(path)
        for prefix, sub_structure in structure.items():
            # print(' ' * level, prefix)
            key = prefix
            if level > 2:
                key = str(ord(prefix[-1]))
            new_path = join(path, key)
            if type(sub_structure) == dict:
                print(' ' * level, prefix)
                self.create_dir(new_path, sub_structure, level + 1)
            else:
                if exists(new_path):
                    raise StorageError(f"File shouldn't exist: '{new_path}'")
                self.save_data(new_path, prefix, sub_structure)
                copy(new_path, f'{new_path}.bak')
                if self.splitting:
                    copy(new_path, f'{new_path}.new')

    def save_data(self, path, prefix, titles):
        raise NotImplementedError()


class SimpleStorageBuilder(BaseStorageBuilder):
    def save_data(self, path, prefix, titles):
        lines = [f'{title}\t{self.data(title)}' for title in sorted(titles)]
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
