from lib.parse.groupers.base import BaseGrouper


class HomonymsGrouper(BaseGrouper):
    fields = ('lang', 'homonym')

    def __init__(self, langs):
        super().__init__()
        self.langs = langs

    def __iter__(self):
        for lang, language in self.langs.items():
            for homonym_header, homonym in language.homonyms.items():
                key = (lang, homonym_header)
                yield key, homonym

    def all(self):
        return self.grouped(like_items=True, unique=True)
