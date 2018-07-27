from lib.parse.groupers.sections.base import BaseSectionsGrouper


class HomonymsGrouper(BaseSectionsGrouper):
    def __init__(self, base):
        super().__init__(base)
        types = {
            'Page': {'level': 2, 'fields': ('lang', 'homonym')},
            'LanguageSection': {'level': 1, 'fields': ('homonym', )},
        }
        base_type = type(base).__name__  # get class name
        if base_type not in types:
            # try to get parent class (e.g. useful for StoragePage etc.)
            base_type = type(base).__bases__[0].__name__
        self.level = types[base_type]['level']
        self.fields = types[base_type]['fields']

    def __iter__(self):
        for path, homonym in self.base.deep(self.level):
            yield path, homonym

    def all(self):
        return self.grouped(like_items=True, unique=True)
