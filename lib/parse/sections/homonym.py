from lib.parse.sections.base import BaseSection
from lib.parse.sections.block import BlockSection
from lib.parse.patterns import R, TR
from lib.parse.sections.grouper_mixins.blocks import BlocksGroupersMixin
from lib.parse.utils.iterators import DeepIterator


class HomonymSection(BlocksGroupersMixin, DeepIterator, BaseSection):
    fields = ('block', )

    parse_pattern = R.third_header
    child_section_type = BlockSection

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)

        if self.header == '':
            self._key = ''
        else:
            m = TR.homonym_header.match(self.header)
            if not m:
                raise Exception()
            self._key = m.group('args')
