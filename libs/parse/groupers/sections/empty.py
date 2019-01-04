from libs.parse.groupers.sections.base import BaseSectionsGrouper


class EmptyBaseSectionsGrouper(BaseSectionsGrouper):
    fields = ()

    def __init__(self, base):
        super().__init__(base)
        self.content = ''

    def __iter__(self):
        yield from ()
