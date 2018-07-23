from lib.parse.sections.base import BaseSection
from lib.parse.utils.decorators import parsed
from lib.parse.sections.block import BlockSection
from lib.parse.patterns import R
from lib.parse.utils.iterators import DeepIterator


class HomonymSection(BaseSection, DeepIterator):
    parse_pattern = R.third_header
    child_section_type = BlockSection

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)
        # todo: сгенерировать `self._key` попроще

    @property
    @parsed
    def blocks(self):
        return self.sub_sections

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
