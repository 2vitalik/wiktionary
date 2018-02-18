from os.path import join, exists, isfile

from lib.storage.blocks.content import ContentsBlock
from lib.storage.blocks.simple import SimpleBlock
from lib.storage.const import MAX_DEPTH
from lib.storage.error import StorageError
from lib.utils.unicode import char_info


class BaseStorageHandler:
    block_class = None

    def __init__(self, path, max_count):
        self.path = path
        self.max_count = max_count

    def block(self, title):
        if not self.block_class:
            raise NotImplementedError('You need set `block_class` attribute')
        path = self.block_path(title)
        return self.block_class(path, title, self)

    def get(self, title):
        return self.block(title).get()

    def update(self, title, value):
        self.block(title).update(value)

    def delete(self, title):
        self.block(title).delete()

    def block_path(self, title):
        category, name = char_info(title[0])

        candidates = [
            join(self.path, category),
            join(self.path, category, name),
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


class ContentStorageHandler(BaseStorageHandler):
    block_class = ContentsBlock

    # todo: Использовать `cache` для ускорения массового считывания


class SimpleStorageHandler(BaseStorageHandler):
    block_class = SimpleBlock
