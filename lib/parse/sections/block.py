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
