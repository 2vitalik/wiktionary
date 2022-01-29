from libs.parse.tests.classes.groupers.base_groupers import BaseSectionsGrouper


class BaseSection(BaseSectionsGrouper):
    is_leaf = False

    parse_pattern = None
    child_section_type = None

    copy_top_to_sub_sections = False

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(base)

        self.title = ...  # из base.title, если есть

        self.full_header = full_header
        self.header = header
        self.content = content
        self.silent = silent

        self.is_parsing = False
        self.parsed = False

        self._key = None
        self._top = None  # плюс свойство `top`
        self._sub_sections = None  # плюс свойство `sub_sections`
        self._old_content = content

    def __eq__(self, other):
        ...  # сравнение по (full_header, header, content)

    def __bool__(self):
        ...  # всегда True

    @property
    def key(self):
        return ...  # _key или header или title

    @property
    def keys(self):
        return ...  # _sub_sections.keys()

    def __getitem__(self, index):
        ...

    def __getattr__(self, attr):
        ...

    def __iter__(self):
        ...

    def sub_sections_content(self):
        ...

    @property
    def new_content(self):
        return ...
