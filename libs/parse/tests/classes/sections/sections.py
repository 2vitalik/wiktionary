from libs.parse.tests.classes.sections.base_section import BaseSection
from libs.parse.tests.classes.sections.groupers_mixins import \
    HomonymsGroupersMixin, LanguagesGrouperMixin, BlocksGroupersMixin, \
    SubBlocksGroupersMixin


class Page(LanguagesGrouperMixin, DeepIterator, BaseSection):
    fields = ('lang',)

    def __init__(self, title, content, is_redirect=None, silent=False):
        super().__init__(base=None, full_header=None, header=None, _=...)

        self.title = title
        self.is_redirect = is_redirect  # todo: implement in inheritors
        self.is_category = title.startswith(u'Категория:')
        self.is_template = title.startswith(u'Шаблон:')

    def upload_changes(self, desc, minor=True, debug=False):
        ...


class LanguageSection(HomonymsGroupersMixin, DeepIterator, BaseSection):
    fields = ('homonym',)

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(...)

        self._key = ...


class HomonymSection(BlocksGroupersMixin, DeepIterator, BaseSection):
    fields = ('block',)

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(...)

        self._key = ...


class BlockSection(SubBlocksGroupersMixin, DeepIterator, BaseSection):
    fields = ('sub_block', )
    copy_top_to_sub_sections = True

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(...)

        self._key = ...


class SubBlockSection(BaseSection):
    is_leaf = True
    copy_top_to_sub_sections = True

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(...)

        self._key = ...
