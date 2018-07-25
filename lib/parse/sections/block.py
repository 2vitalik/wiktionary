from lib.parse.sections.base import BaseSection
from lib.parse.sections.grouper_mixins.sub_blocks import SubBlocksGroupersMixin
from lib.parse.sections.sub_block import SubBlockSection
from lib.parse.patterns import R, H
from lib.parse.utils.iterators import DeepIterator


class BlockSection(SubBlocksGroupersMixin, DeepIterator, BaseSection):
    parse_pattern = R.forth_header
    child_section_type = SubBlockSection

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)
        self._key = H.get_key(header)
