from lib.parse.groupers.sections.base import BaseSectionsGrouper


class EmptyBaseSectionsGrouper(BaseSectionsGrouper):
    fields = ()

    def __init__(self):
        super().__init__(self)

    def __iter__(self):
        yield from ()
