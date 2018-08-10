from libs.parse.sections.base import BaseSection
from libs.parse.sections.grouper_mixins.homonyms import HomonymsGroupersMixin
from libs.parse.sections.homonym import HomonymSection
from libs.parse.patterns import TR, R
from libs.parse.utils.iterators import DeepIterator


class LanguageSection(HomonymsGroupersMixin, DeepIterator, BaseSection):
    fields = ('homonym', )

    parse_pattern = R.second_header
    child_section_type = HomonymSection

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(base, full_header, header, content, silent)

        if self.header == '':
            self._key = ''
        else:
            m = TR.lang_header.match(self.header)
            if m:
                self._key = m.group('lang')
            else:
                if self.silent:
                    self._key = self.header
                else:
                    raise Exception(f'Wrong first header: "{self.header}" '
                                    f'in "{self.title}"')
