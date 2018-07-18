from lib.parse.groupers.base import BaseGrouper


class HomonymsGrouper(BaseGrouper):
    fields = ('lang', 'homonym')

    def __init__(self, page):
        super().__init__()
        self.page = page

    def __iter__(self):
        for (lang, homonym_header), homonym in self.page.deep(2):
            key = (lang, homonym_header)
            yield key, homonym

    def all(self):
        return self.grouped(like_items=True, unique=True)
