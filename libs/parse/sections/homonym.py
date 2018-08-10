from libs.parse.sections.base import BaseSection
from libs.parse.sections.block import BlockSection
from libs.parse.patterns import R, TR
from libs.parse.sections.grouper_mixins.blocks import BlocksGroupersMixin
from libs.parse.utils.iterators import DeepIterator


class HomonymSection(BlocksGroupersMixin, DeepIterator, BaseSection):
    fields = ('block', )

    parse_pattern = R.third_header
    child_section_type = BlockSection

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(base, full_header, header, content, silent)

        if self.header == '':
            self._key = ''
        else:
            m = TR.homonym_header.match(self.header)
            if m:
                self._key = m.group('args')
            else:
                if self.silent:
                    self._key = self.header
                else:
                    raise Exception(f'Wrong homonym header: "{self.header}"')
