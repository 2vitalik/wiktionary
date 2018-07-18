from lib.parse.utils.decorators import parsed, parsing
from lib.parse.sections.sub_block import SubBlockSection
from lib.parse.patterns import P
from lib.utils.collection import chunks


class BlockSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._sub_blocks = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def sub_blocks(self):
        return self._sub_blocks

    @parsed
    def __iter__(self):
        for sub_header, sub_block in self.sub_blocks.items():
            yield sub_header, sub_block

    @parsed
    def __getitem__(self, key):
        if key in self.sub_blocks:
            return self.sub_blocks[key]
        if type(key) == int:
            index = int(key)
            lang = list(self.sub_blocks.keys())[index]
            return self.sub_blocks[lang]
        # if key in self.headers:
        #     return Lan

    @parsed
    def __getattr__(self, key):
        if key in self.sub_blocks:
            return self.sub_blocks[key]

    @parsing
    def _parse(self):
        parts = P.forth_header.split(self.content)
        if len(parts) == 1:
            self._sub_blocks = {
                '': SubBlockSection(self, '', '', parts[0]),
            }
            return
        self._top = parts.pop(0)
        self._sub_blocks = dict()
        for header, value, content in chunks(parts, 3):
            if value in self._sub_blocks:
                raise Exception(f'Duplicated sub-block on the page '
                                f'"{self.title}"')
            self._sub_blocks[value] = \
                SubBlockSection(self, header, value, content)
