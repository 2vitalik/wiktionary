from lib.utils.collection import group


class BaseGrouper:
    fields = None

    def __init__(self, base):
        self.base = base
        self._cache = {}

    @property
    def keys(self):
        return self.base.keys

    def values(self, *args, unique=False):
        return self.grouped(*args, like_items=False, unique=unique)

    def items(self, *args, unique=False):
        return self.grouped(*args, like_items=True, unique=unique)

    def grouped(self, *args, like_items, unique):
        if args == ('*', ):
            args = self.fields
        if like_items and len(args) == len(self.fields):
            args = args[:-1]  # because last layer will be redundant
        if self._cache.get(args) is None:
            indexes = [self.fields.index(arg) for arg in args]
            self._cache[args] = group(self, indexes, like_items, unique)
        return self._cache[args]
