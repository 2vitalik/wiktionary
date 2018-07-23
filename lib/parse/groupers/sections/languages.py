from lib.parse.groupers.sections.base import BaseSectionsGrouper


class LanguagesGrouper(BaseSectionsGrouper):
    fields = ('lang', )

    def __init__(self, page):
        super().__init__()
        self.page = page

    def __iter__(self):
        for lang, lang_section in self.page.deep(1):
            path = (lang, )
            yield path, lang_section

    def all(self):
        return self.grouped(like_items=True, unique=True)
