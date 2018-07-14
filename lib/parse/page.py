from lib.parse.patterns import P
from lib.utils.collection import chunks


class BasePage:
    def __init__(self, title, content, is_redirect=None):
        self.title = title
        self.content = content
        self.is_redirect = is_redirect  # todo: implement in inheritors
        self.is_category = title.startswith(u'Категория:')
        self.is_template = title.startswith(u'Шаблон:')
        self._parse()

    def _parse(self):
        parts = P.lang_header.split(self.content)
        self.top = parts.pop(0)
        self.langs_order = list()
        self.langs = dict()
        for header, lang, content in chunks(parts, 3):
            self.langs_order.append(lang)
            if lang in self.langs:
                # todo: create special DuplicatedException(type, title)
                raise Exception(f'Duplicated language on the page '
                                f'"{self.title}"')
            self.langs[lang] = LanguageSection(self, header, lang, content)


class LanguageSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content
        self._parse()

    def _parse(self):
        parts = P.second_header.split(self.content)
        if len(parts) == 1:
            self.homonyms_order = ['']
            self.homonyms = {
                '': HomonymSection(self, '', '', parts[0]),
            }
            return
        self.top = parts.pop(0)
        self.homonyms_order = list()
        self.homonyms = dict()
        for header, value, content in chunks(parts, 3):
            self.homonyms_order.append(value)
            if value in self.homonyms:
                raise Exception(f'Duplicated homonym on the page '
                                f'"{self.title}"')
            self.homonyms[value] = HomonymSection(self, header, value, content)


class HomonymSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content
        self._parse()

    def _parse(self):
        parts = P.third_header.split(self.content)
        if len(parts) == 1:
            self.blocks_order = ['']
            self.blocks = {
                '': BlockSection(self, '', '', parts[0]),
            }
            return
        self.top = parts.pop(0)
        self.blocks_order = list()
        self.blocks = dict()
        for header, value, content in chunks(parts, 3):
            self.blocks_order.append(value)
            if value in self.blocks:
                raise Exception(f'Duplicated block on the page "{self.title}"')
            self.blocks[value] = BlockSection(self, header, value, content)


class BlockSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content
        self._parse()

    def _parse(self):
        parts = P.forth_header.split(self.content)
        if len(parts) == 1:
            self.sub_blocks_order = ['']
            self.sub_blocks = {
                '': SubBlockSection(self, '', '', parts[0]),
            }
            return
        self.top = parts.pop(0)
        self.sub_blocks_order = list()
        self.sub_blocks = dict()
        for header, value, content in chunks(parts, 3):
            self.sub_blocks_order.append(value)
            if value in self.sub_blocks:
                raise Exception(f'Duplicated sub-block on the page '
                                f'"{self.title}"')
            self.sub_blocks[value] = \
                SubBlockSection(self, header, value, content)


class SubBlockSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content


# todo: методы, позволяющие получить ту или иную инфу
# todo: check for strange headers on first level
# todo: override `__getitem__` for all sections, and also iterator list(...)
