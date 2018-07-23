from lib.parse.sections.base import BaseSection
from lib.parse.utils.decorators import parsed
from lib.parse.sections.sub_block import SubBlockSection
from lib.parse.patterns import R
from lib.parse.utils.iterators import DeepIterator


class BlockSection(BaseSection, DeepIterator):
    parse_pattern = R.forth_header
    child_section_type = SubBlockSection

    @property
    @parsed
    def sub_blocks(self):
        return self.sub_sections

    @parsed
    def __getitem__(self, key):
        if key in self.sub_blocks:
            return self.sub_blocks[key]
        if type(key) == int:
            index = int(key)
            lang = list(self.sub_blocks.keys())[index]
            return self.sub_blocks[lang]

    @parsed
    def __getattr__(self, key):
        if key in self.sub_blocks:
            return self.sub_blocks[key]
