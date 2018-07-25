from lib.parse.sections.base import BaseSection
from lib.parse.sections.block import BlockSection
from lib.parse.patterns import R
from lib.parse.sections.grouper_mixins.blocks import BlocksGroupersMixin
from lib.parse.utils.iterators import DeepIterator


class HomonymSection(BlocksGroupersMixin, DeepIterator, BaseSection):
    parse_pattern = R.third_header
    child_section_type = BlockSection

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)
        # todo: сгенерировать `self._key` попроще
