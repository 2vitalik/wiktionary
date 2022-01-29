from libs.parse.groupers.sections.base import BaseSectionsGrouper


class LanguagesGrouper(BaseSectionsGrouper):
    fields = ('lang', )

    def __iter__(self):
        for _, lang_section in self.iterate():
            yield lang_section

    def iterate(self):
        for lang, lang_section in self.base.deep(1):
            path = (lang, )
            yield path, lang_section

    def all(self):
        return self.grouped(last_dict=True, unique=True)
