from lib.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from lib.parse.utils.decorators import parsed, parsing
from lib.parse.sections.homonym import HomonymSection
from lib.parse.patterns import P
from lib.parse.utils.iterators import DeepIterator
from lib.utils.collection import chunks


class LanguageSection(DeepIterator):
    def __init__(self, base, wiki_header, lang, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.lang = lang
        self.content = content

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._homonyms = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def homonyms(self):
        return self._homonyms

    @parsed
    def __iter__(self):
        for homonym_header, homonym in self.homonyms.items():
            yield homonym_header, homonym

    @parsed
    def __getitem__(self, key):
        if key in self.homonyms:
            return self.homonyms[key]
        if type(key) == int:
            index = int(key)
            header = list(self.homonyms.keys())[index]
            return self.homonyms[header]
        # if key in self.headers:
        #     return AnyBlocksGrouper(self, self.headers[key])  # todo

    @parsed
    def __getattr__(self, key):
        if key in self.homonyms:
            return self.homonyms[key]

    @parsing
    def _parse(self):
        parts = P.second_header.split(self.content)
        if len(parts) == 1:
            self._homonyms = {
                '': HomonymSection(self, '', '', parts[0]),
            }
            return
        self._top = parts.pop(0)
        self._homonyms = dict()
        for header, value, content in chunks(parts, 3):
            if value in self._homonyms:
                raise Exception(f'Duplicated homonym on the page '
                                f'"{self.title}"')
            self._homonyms[value] = HomonymSection(self, header, value, content)
