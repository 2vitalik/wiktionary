from lib.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from lib.parse.groupers.sections.blocks.blocks import BlocksGrouper
from lib.parse.groupers.sections.blocks.sub_blocks import SubBlocksGrouper
from lib.parse.sections.base import BaseSection
from lib.parse.utils.decorators import parsed
from lib.parse.sections.homonym import HomonymSection
from lib.parse.patterns import TR, R
from lib.parse.utils.iterators import DeepIterator


class LanguageSection(BaseSection, DeepIterator):
    parse_pattern = R.second_header
    child_section_type = HomonymSection

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)

        m = TR.lang_header.match(self.header)
        if not m:
            raise Exception
        self._key = m.group('lang')

    @property
    @parsed
    def homonyms(self):
        return self.sub_sections

    @parsed
    def blocks(self):
        return BlocksGrouper(self)

    @parsed
    def any_blocks(self):
        return AnyBlocksGrouper(self)

    @parsed
    def sub_blocks(self):
        return SubBlocksGrouper(self)

    @parsed
    def __getitem__(self, key):
        if key in self.homonyms:
            return self.homonyms[key]
        if type(key) == int:
            index = int(key)
            header = list(self.homonyms.keys())[index]
            return self.homonyms[header]
        # if key in self.headers:
        #     return AnyBlocksGrouper(self, self.headers[key])  # todo

    @parsed
    def __getattr__(self, key):
        if key in self.homonyms:
            return self.homonyms[key]
