from lib.parse.sections.base import BaseSection
from lib.parse.sections.grouper_mixins.homonyms import HomonymsGroupersMixin
from lib.parse.sections.homonym import HomonymSection
from lib.parse.patterns import TR, R
from lib.parse.utils.iterators import DeepIterator


class LanguageSection(HomonymsGroupersMixin, DeepIterator, BaseSection):
    parse_pattern = R.second_header
    child_section_type = HomonymSection

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)

        m = TR.lang_header.match(self.header)
        if not m:
            raise Exception
        self._key = m.group('lang')
