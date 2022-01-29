from libs.utils.collection import group


class BaseGrouper:
    fields = None  # should be set in inheritance

    def __init__(self, base):
        self.base = base
        self._cache = {}

    def __str__(self):
        name = type(self).__name__
        base_name = type(self.base).__name__ if self.base else None
        return f"{name}({base_name})"

    def __len__(self):
        if not self.base:
            return 0
        return len(self.base)

    def __getitem__(self, item):
        return self.base[item]

    @property
    def keys(self):
        return self.base.keys

    # todo: add `as_list` as last_list()  # with no args

    def last_list(self, *args, unique=False):
        return self.grouped(*args, last_dict=False, unique=unique)

    def last_dict(self, *args, unique=False):
        return self.grouped(*args, last_dict=True, unique=unique)

    # todo: add `last_items` as `last_dict(...).items()`

    def grouped(self, *args, last_dict, unique):
        if args == ('*', ):
            args = self.fields
        if last_dict and len(args) == len(self.fields):
            args = args[:-1]  # because last layer will be redundant

        cache_key = (args, last_dict, unique)
        if self._cache.get(cache_key) is None:
            indexes = [self.fields.index(arg) for arg in args]
            self._cache[cache_key] = group(self, indexes, last_dict, unique)

        return self._cache[cache_key]

    def __getattr__(self, item):
        pass  # todo
