from lib.parse.utils.decorators import parsed, parsing
from lib.parse.sections.block import BlockSection
from lib.parse.patterns import P
from lib.parse.utils.iterators import DeepIterator
from lib.utils.collection import chunks


class HomonymSection(DeepIterator):
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._blocks = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def blocks(self):
        return self._blocks

    @parsed
    def __iter__(self):
        for header, block in self.blocks.items():
            yield header, block

    @parsed
    def __getitem__(self, key):
        if key in self.blocks:
            return self.blocks[key]
        if type(key) == int:
            index = int(key)
            lang = list(self.blocks.keys())[index]
            return self.blocks[lang]

    @parsed
    def __getattr__(self, key):
        if key in self.blocks:
            return self.blocks[key]

    @parsing
    def _parse(self):
        parts = P.third_header.split(self.content)
        if len(parts) == 1:
            self._blocks = {
                '': BlockSection(self, '', '', parts[0]),
            }
            return
        self._top = parts.pop(0)
        self._blocks = dict()
        for header, value, content in chunks(parts, 3):
            if value in self._blocks:
                raise Exception(f'Duplicated block on the page "{self.title}"')
            self._blocks[value] = BlockSection(self, header, value, content)
