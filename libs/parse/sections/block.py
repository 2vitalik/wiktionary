from libs.parse.sections.base import BaseSection
from libs.parse.sections.grouper_mixins.sub_blocks import SubBlocksGroupersMixin
from libs.parse.sections.sub_block import SubBlockSection
from libs.parse.patterns import R, H
from libs.parse.utils.iterators import DeepIterator


class BlockSection(SubBlocksGroupersMixin, DeepIterator, BaseSection):
    fields = ('sub_block', )

    parse_pattern = R.forth_header
    child_section_type = SubBlockSection
    copy_top_to_sub_sections = True

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(base, full_header, header, content, silent)
        self._key = H.get_key(header)
