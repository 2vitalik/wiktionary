from lib.parse.sections.base import BaseSection
from lib.parse.sections.grouper_mixins.languages import LanguagesGrouperMixin
from lib.parse.patterns import R
from lib.parse.sections.language import LanguageSection
from lib.parse.utils.iterators import DeepIterator


class Page(LanguagesGrouperMixin, DeepIterator, BaseSection):
    fields = ('lang', )

    parse_pattern = R.first_header
    child_section_type = LanguageSection

    def __init__(self, title, content, is_redirect=None):
        super().__init__(None, None, None, content)
        self.title = title
        self.is_redirect = is_redirect  # todo: implement in inheritors
        self.is_category = title.startswith(u'Категория:')
        self.is_template = title.startswith(u'Шаблон:')
