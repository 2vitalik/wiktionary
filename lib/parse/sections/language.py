from lib.parse.sections.base import BaseSection
from lib.parse.sections.grouper_mixins.homonyms import HomonymsGroupersMixin
from lib.parse.utils.decorators import parsed
from lib.parse.sections.homonym import HomonymSection
from lib.parse.patterns import TR, R
from lib.parse.utils.iterators import DeepIterator


class LanguageSection(BaseSection, HomonymsGroupersMixin, DeepIterator):
    parse_pattern = R.second_header
    child_section_type = HomonymSection

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)

        m = TR.lang_header.match(self.header)
        if not m:
            raise Exception
        self._key = m.group('lang')

    @parsed
    def __getitem__(self, index):
        result = super().__getitem__(index)
        if result is not None:
            return result
        # if index in self.headers:
        #     return AnyBlocksGrouper(self, self.headers[index])  # todo
