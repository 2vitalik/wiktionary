from libs.utils.collection import group


class BaseGrouper:
    fields = None

    def __init__(self, base):
        self.base = base
        self._cache = {}

    def __len__(self):
        if not self.base:
            return 0
        return len(self.base)

    def __getitem__(self, item):
        return self.base[item]

    @property
    def keys(self):
        return self.base.keys

    def as_list(self, *args, unique=False):
        return self.grouped(*args, like_items=False, unique=unique)

    def as_dict(self, *args, unique=False):
        return self.grouped(*args, like_items=True, unique=unique)

    def grouped(self, *args, like_items, unique):
        if args == ('*', ):
            args = self.fields
        if like_items and len(args) == len(self.fields):
            args = args[:-1]  # because last layer will be redundant
        cache_key = (args, like_items, unique)
        if self._cache.get(cache_key) is None:
            indexes = [self.fields.index(arg) for arg in args]
            self._cache[cache_key] = group(self, indexes, like_items, unique)
        return self._cache[cache_key]

    def __getattr__(self, item):
        pass  # todo
