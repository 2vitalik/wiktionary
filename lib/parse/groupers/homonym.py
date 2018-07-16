class HomonymsGrouper:
    def __init__(self, langs):
        self.langs = langs

    @property
    def all(self):
        data = {}
        for lang, lang_section in self.langs.items():
            for homonym, homonym_section in lang_section.homonyms.items():
                key = (lang, homonym)
                data[key] = homonym_section
        return data

    @property
    def grouped(self):
        data = {}
        for lang, lang_section in self.langs.items():
            data[lang] = dict()
            for homonym, homonym_section in lang_section.homonyms.items():
                data[lang][homonym] = homonym_section
        return data
