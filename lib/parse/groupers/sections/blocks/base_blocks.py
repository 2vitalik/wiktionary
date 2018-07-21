from lib.parse.groupers.sections.base import BaseSectionsGrouper


class BaseBlocksGrouper(BaseSectionsGrouper):
    def __init__(self, base, header=None, no_sub_blocks=False):
        super().__init__()
        self.base = base  # object we're searching in
        self.header = header  # header we're searching for
        types = {
            'Page': {'level': 3,
                     'fields': ('lang', 'homonym', 'block', 'sub_block')},
            'Language': {'level': 2,
                         'fields': ('homonym', 'block', 'sub_block')},
            'Homonym': {'level': 1,
                        'fields': ('block', 'sub_block')},
        }
        if no_sub_blocks:
            del types['Homonym']  # because we have just attr `blocks` there
        base_type = type(base).__name__  # get class name
        if base_type not in types:
            # try to get parent class (e.g. useful for StoragePage etc.)
            base_type = type(base).__bases__[0].__name__
        self.level = types[base_type]['level']
        self.fields = types[base_type]['fields']
        if no_sub_blocks:
            self.fields = self.fields[:-1]  # remove 'sub_block'
        if self.header:
            self.fields = self.fields[:-1]  # because last entry always the same

    def all(self):
        return self.grouped(like_items=True, unique=True)
