from os.path import join, exists, isfile

from lib.storage.const import MAX_DEPTH
from lib.storage.error import StorageError
from lib.utils.io import write
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
            (category, join(self.handler.path, category)),
            (name, join(self.handler.path, category, name)),
        ]

        path = candidates[-1][1]
        for i in range(MAX_DEPTH):
            code = ord(title[i]) if i < len(title) else 0
            key = f'{code} - {hex(code)}'

            key = str(hex(ord(title[i])))  # код соответствующего символа
            path = join(path, key)
            candidates.append((title[:i + 1], path))

        for prefix, candidate in candidates:
            if not exists(candidate):
                write(candidate, f"Prefix: {prefix}")
                return candidate
            if isfile(candidate):
                return candidate

        raise StorageError(f"Path does't exist for title '{title}'")
