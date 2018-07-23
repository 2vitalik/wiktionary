from lib.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from lib.parse.sections.base import BaseSection
from lib.parse.sections.grouper_mixins.languages import LanguagesGrouperMixin
from lib.parse.utils.decorators import parsed
from lib.parse.patterns import R
from lib.parse.sections.language import LanguageSection
from lib.parse.utils.iterators import DeepIterator


class Page(BaseSection, LanguagesGrouperMixin, DeepIterator):
    parse_pattern = R.first_header
    child_section_type = LanguageSection

    headers = {
        'morphology': 'Морфологические и синтаксические свойства',
        # ...
    }
    morphology = headers['morphology']
    # ...

    def __init__(self, title, content, is_redirect=None):
        super().__init__(None, None, None, content)
        self.title = title
        self.is_redirect = is_redirect  # todo: implement in inheritors
        self.is_category = title.startswith(u'Категория:')
        self.is_template = title.startswith(u'Шаблон:')

    @parsed
    def __getitem__(self, index):
        result = super().__getattr__(index)
        if result is not None:
            return result
        if index in self.headers:
            return AnyBlocksGrouper(self, self.headers[index])
        return AnyBlocksGrouper(self, index)

    @parsed
    def __getattr__(self, attr):
        result = super().__getattr__(attr)
        if result is not None:
            return result
        if attr in self.headers:
            return AnyBlocksGrouper(self, self.headers[attr])
