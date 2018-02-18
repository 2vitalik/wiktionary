from os.path import join, exists, isfile

from lib.storage.const import MAX_DEPTH
from lib.storage.error import StorageError
from lib.utils.unicode import char_info


class BaseBlock:
    def __init__(self, title, handler):
        self.title = title
        self.handler = handler
        self.path = self.block_path(title)

    def get(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def update(self, value):
        raise NotImplementedError()

    def block_path(self, title):
        category, name = char_info(title[0])

        candidates = [
            join(self.handler.path, category),
            join(self.handler.path, category, name),
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
