

class BaseGrouper:
    fields = ...  # should be set in inheritance

    def __init__(self, base):
        self.base = base  # это section
        ...

    def __len__(self):
        ...

    def __getitem__(self, item):
        ...

    @property
    def keys(self):
        return self.base.keys  # keys у section

    def last_list(self, *args, unique=False):
        return self.grouped(*args, last_dict=False, unique=unique)

    def last_dict(self, *args, unique=False):
        return self.grouped(*args, last_dict=True, unique=unique)

    # todo: add `last_items` as `last_dict(...).items()`!!

    def grouped(self, *args, last_dict, unique):
        ...

    def __getattr__(self, item):
        ...  # todo


class BaseSectionsGrouper(BaseGrouper):
    @property
    def templates(self):
        return TemplatesGrouper(self)
