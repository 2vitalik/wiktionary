from libs.parse.data.page import PageData
from libs.parse.patterns import R
from libs.parse.sections.base import BaseSection
from libs.parse.sections.grouper_mixins.languages import LanguagesGrouperMixin
from libs.parse.sections.language import LanguageSection
from libs.parse.utils.iterators import DeepIterator
from libs.utils.wikibot import load_page, save_page


class Page(LanguagesGrouperMixin, DeepIterator, BaseSection):
    fields = ('lang',)

    parse_pattern = R.first_header
    child_section_type = LanguageSection

    def __init__(self, title, content, site_lang: str, is_redirect=None, silent=False):
        super().__init__(base=None, full_header=None, header=None,
                         content=content, silent=silent)
        self.site_lang: str = site_lang
        self.title = title
        self.is_redirect = is_redirect  # todo: implement in inheritors
        self.is_category = title.startswith(u'Категория:')
        self.is_template = title.startswith(u'Шаблон:')
        self.data = PageData(self)

    def upload_changes(self, desc, minor=True, debug=False):
        server_content = load_page(self.title)
        if server_content != self._old_content:
            raise Exception('Content on the server was suddenly changed.')
        new_content = self.new_content
        if new_content != self._old_content:
            if debug:
                print('=' * 10)
                print(self.title)
                print('-' * 10)
                print(new_content)
                print('-' * 10)
                return
            save_page(self.title, new_content, desc, minor, check_changes=False)
