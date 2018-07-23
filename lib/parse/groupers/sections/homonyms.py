from lib.parse.groupers.sections.base import BaseSectionsGrouper


class HomonymsGrouper(BaseSectionsGrouper):
    fields = ('lang', 'homonym')

    def __init__(self, page):
        super().__init__()
        self.page = page

    def __iter__(self):
        for (lang, homonym_header), homonym in self.page.deep(2):
            path = (lang, homonym_header)
            yield path, homonym

    def all(self):
        return self.grouped(like_items=True, unique=True)
