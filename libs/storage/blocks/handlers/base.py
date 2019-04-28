from os.path import join, exists, isfile

from libs.storage.const import MAX_DEPTH
from libs.storage.error import BlockNotFound
from libs.utils.cache import Cache
from libs.utils.exceptions import LockedError
from libs.utils.io import write, is_locked, lock_file, unlock_file
from libs.utils.unicode import char_info


class BaseBlockHandler:
    """
    ...
    Комментарий по поводу `lock` механизма:
    - в наследниках нужно делать self.unlock() после `delete()` или `update()`
    """
    cache = Cache(400)

    def __init__(self, title, handler, lock=False):
        self.title = title
        self.handler = handler
        try:
            self.path = self.old_block_path(title)
        except BlockNotFound:
            self.path = self.block_path(title)
        if is_locked(self.path):
            raise LockedError(self.path)  # todo: several attempts
        self.locked = lock
        if lock:
            self.lock()

        data = self.cache.get(self.path)
        if data:
            self.contents, self.titles = data
        else:
            self.contents, self.titles = None, None
            self.get_contents_and_title()
            self.cache.update(self.path, (self.contents, self.titles))

    def get_contents_and_title(self):
        raise NotImplementedError()

    def lock(self):
        lock_file(self.path)

    def unlock(self):
        if self.locked:
            unlock_file(self.path)
        self.locked = False

    def default_empty(self, prefix):
        raise NotImplementedError()

    def get(self, silent=False):
        raise NotImplementedError()

    def delete(self):
        self.do_delete()
        self.unlock()

    def update(self, value):
        self.do_update(value)
        self.unlock()

    def save(self):
        self.cache.remove(self.path)

    def do_delete(self):
        raise NotImplementedError()

    def do_update(self, value):
        raise NotImplementedError()

    def old_block_path(self, title):  # todo: remove
        category, name = char_info(title[0])

        candidates = [
            (category, join(self.handler.path, category)),
            (name, join(self.handler.path, category, name)),
        ]

        path = candidates[-1][1]
        for i in range(MAX_DEPTH):
            code = ord(title[i]) if i < len(title) else 0
            key = f'{code} - {hex(code)}'
            path = join(path, key)
            candidates.append((title[:i + 1], path))

        for prefix, candidate in candidates:
            if not exists(candidate):
                raise BlockNotFound(f"Path does't exist for title '{title}'")
            if is_locked(candidate):
                raise LockedError(candidate)  # todo: several attempts
            if isfile(candidate):
                return candidate

        raise BlockNotFound(f"Path does't exist for title '{title}'")

    def block_path(self, title):
        category, name = char_info(title[0])
        if category not in ['Ll', 'Lo', 'Lu', 'Pd']:
            name = 'OTHER'
        candidates = [
            (name, join(self.handler.path, name)),
        ]

        path = candidates[-1][1]
        for i in range(MAX_DEPTH):
            code = ord(title[i]) if i < len(title) else 0
            key = f'{code} - {hex(code)}'
            path = join(path, key)
            candidates.append((title[:i + 1], path))

        for prefix, candidate in candidates:
            if not exists(candidate):
                print(f"`write`: {candidate}")
                write(candidate, self.default_empty(prefix))
                return candidate
            if is_locked(candidate):
                raise LockedError(candidate)  # todo: several attempts
            if isfile(candidate):
                return candidate

        raise BlockNotFound(f"Path does't exist for title '{title}'")  # fixme: never should happen?
