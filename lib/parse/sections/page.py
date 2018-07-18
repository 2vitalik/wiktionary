from lib.parse.groupers.block import BlocksGrouper
from lib.parse.utils.decorators import parsed, parsing
from lib.parse.groupers.homonym import HomonymsGrouper
from lib.parse.patterns import P
from lib.parse.sections.language import LanguageSection
from lib.parse.utils.iterators import DeepIterator
from lib.utils.collection import chunks


class Page(DeepIterator):
    headers = {
        'morphology': 'Морфологические и синтаксические свойства',
        # ...
    }
    morphology = headers['morphology']
    # ...

    def __init__(self, title, content, is_redirect=None):
        self.title = title
        self.content = content
        self.is_redirect = is_redirect  # todo: implement in inheritors
        self.is_category = title.startswith(u'Категория:')
        self.is_template = title.startswith(u'Шаблон:')

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._langs = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def langs(self):
        return self._langs

    @parsed
    def __iter__(self):
        for lang, language in self.langs.items():
            yield lang, language

    @property
    @parsed
    def homonyms(self):
        return HomonymsGrouper(self)

    @parsed
    def __getitem__(self, key):
        if key in self.langs:
            return self.langs[key]
        if type(key) == int:
            index = int(key)
            lang = list(self.langs.keys())[index]
            return self.langs[lang]
        if key in self.headers:
            return BlocksGrouper(self, self.headers[key])
        return BlocksGrouper(self, key)

    @parsed
    def __getattr__(self, key):
        if key in self.langs:
            return self.langs[key]

    @parsing
    def _parse(self):
        parts = P.lang_header.split(self.content)
        self._top = parts.pop(0)
        self._langs = dict()
        for header, lang, content in chunks(parts, 3):
            if lang in self._langs:
                # todo: create special DuplicatedException(type, title)
                raise Exception(f'Duplicated language on the page '
                                f'"{self.title}"')
            self._langs[lang] = LanguageSection(self, header, lang, content)
