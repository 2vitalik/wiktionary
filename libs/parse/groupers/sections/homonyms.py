from libs.parse.groupers.sections.base import BaseSectionsGrouper
from libs.utils.debug import debug


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
            if base_type not in types:
                # e.g. for several levels of inheritance
                base_type = type(base).__bases__[0].__bases__[0].__name__
        self.level = types[base_type]['level']
        self.fields = types[base_type]['fields']
        self._debug_init()

    def __iter__(self):
        for _, homonym in self.iterate():
            yield homonym

    def iterate(self):
        self._debug_iter()
        for path, homonym in self.base.deep(self.level):
            yield path, homonym

    def all(self):
        return self.grouped(last_dict=True, unique=True)

    @debug
    def _debug_init(self):
        print(f'- HomonymsGrouper() has created:')
        print(f'  - level: {self.level}')
        print(f'  - fields: {self.fields}')

    @debug
    def _debug_iter(self):
        print(f'- Started iterating through HomonymsGrouper()')
