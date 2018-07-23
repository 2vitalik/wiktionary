from lib.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from lib.parse.sections.base import BaseSection
from lib.parse.utils.decorators import parsed
from lib.parse.groupers.sections.homonyms import HomonymsGrouper
from lib.parse.patterns import R
from lib.parse.sections.language import LanguageSection
from lib.parse.utils.iterators import DeepIterator


class Page(BaseSection, DeepIterator):
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

    @property
    @parsed
    def languages(self):
        return self.sub_sections

    @property
    @parsed
    def homonyms(self):
        return HomonymsGrouper(self)

    @parsed
    def __getitem__(self, key):
        if key in self.languages:
            return self.languages[key]
        if type(key) == int:
            index = int(key)
            lang = list(self.languages.keys())[index]
            return self.languages[lang]
        if key in self.headers:
            return AnyBlocksGrouper(self, self.headers[key])
        return AnyBlocksGrouper(self, key)

    @parsed
    def __getattr__(self, key):
        if key in self.languages:
            return self.languages[key]
