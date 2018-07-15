from lib.parse.patterns import P
from lib.utils.collection import chunks


def parsed(func):
    def wrapped(self, *args, **kwargs):
        if self.is_parsing:
            raise Exception("Can't access an entry which is being parsing "
                            "right now.")
        if not self.parsed:
            self._parse()
        return func(self, *args, **kwargs)
    return wrapped


def parsing(func):
    def wrapped(self, *args, **kwargs):
        self.is_parsing = True
        result = func(self, *args, **kwargs)
        self.parsed = True
        self.is_parsing = False
        return result
    return wrapped


class Page:
    headers = {
        'morphology': 'Морфологические и синтаксические свойства',
        # ...
    }
    morphology = headers['morphology']
    # ...

    def __init__(self, title, content, is_redirect=None):
        self.title = title
        self.content = content
        self.is_redirect = is_redirect  # todo: implement in inheritors
        self.is_category = title.startswith(u'Категория:')
        self.is_template = title.startswith(u'Шаблон:')

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._langs_order = None
        self._langs = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def langs(self):
        return self._langs

    @property
    @parsed
    def langs_order(self):
        return self._langs_order

    # @property
    # @parsed
    # def homonyms_order(self):  # todo
    #     return self....

    @parsed
    def __getitem__(self, key):
        if key in self.langs:
            return self.langs[key]
        if type(key) == int:
            index = int(key)
            lang = self.langs_order[index]
            return self.langs[lang]
        # if key in self.headers:
        #     return Lan...

    @parsed
    def __getattr__(self, key):
        if key in self._langs:
            return self._langs[key]

    @parsing
    def _parse(self):
        parts = P.lang_header.split(self.content)
        self._top = parts.pop(0)
        self._langs_order = list()  # todo: remove all these `order` lists because of Python 3.6 feature
        self._langs = dict()
        for header, lang, content in chunks(parts, 3):
            self._langs_order.append(lang)
            if lang in self._langs:
                # todo: create special DuplicatedException(type, title)
                raise Exception(f'Duplicated language on the page '
                                f'"{self.title}"')
            self._langs[lang] = LanguageSection(self, header, lang, content)


class HomonymsGrouper:  # todo: (new idea)
    def __init__(self):
        pass


class LanguageSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._homonyms_order = None
        self._homonyms = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def homonyms(self):
        return self._homonyms

    @property
    @parsed
    def homonyms_order(self):
        return self._homonyms_order

    @parsed
    def __getitem__(self, key):
        if key in self._homonyms:
            return self._homonyms[key]
        if type(key) == int:
            index = int(key)
            lang = self.homonyms_order[index]
            return self._homonyms[lang]
        # if key in self.headers:
        #     return Lan

    @parsed
    def __getattr__(self, key):
        if key in self._homonyms:
            return self._homonyms[key]

    @parsing
    def _parse(self):
        parts = P.second_header.split(self.content)
        if len(parts) == 1:
            self._homonyms_order = ['']
            self._homonyms = {
                '': HomonymSection(self, '', '', parts[0]),
            }
            return
        self._top = parts.pop(0)
        self._homonyms_order = list()
        self._homonyms = dict()
        for header, value, content in chunks(parts, 3):
            self._homonyms_order.append(value)
            if value in self._homonyms:
                raise Exception(f'Duplicated homonym on the page '
                                f'"{self.title}"')
            self._homonyms[value] = HomonymSection(self, header, value, content)


class HomonymSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content
        self._parse()

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._blocks_order = None
        self._blocks = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def blocks(self):
        return self._blocks

    @property
    @parsed
    def blocks_order(self):
        return self._blocks_order

    @parsed
    def __getitem__(self, key):
        if key in self._blocks:
            return self._blocks[key]
        if type(key) == int:
            index = int(key)
            lang = self.blocks_order[index]
            return self._blocks[lang]
        # if key in self.headers:
        #     return Lan

    @parsed
    def __getattr__(self, key):
        if key in self._blocks:
            return self._blocks[key]

    @parsing
    def _parse(self):
        parts = P.third_header.split(self.content)
        if len(parts) == 1:
            self._blocks_order = ['']
            self._blocks = {
                '': BlockSection(self, '', '', parts[0]),
            }
            return
        self._top = parts.pop(0)
        self._blocks_order = list()
        self._blocks = dict()
        for header, value, content in chunks(parts, 3):
            self._blocks_order.append(value)
            if value in self._blocks:
                raise Exception(f'Duplicated block on the page "{self.title}"')
            self._blocks[value] = BlockSection(self, header, value, content)


class BlockSection:
    def __init__(self, base, wiki_header, header, content):
        self.base = base
        self.title = base.title
        self.wiki_header = wiki_header
        self.header = header
        self.content = content

        self.is_parsing = False
        self.parsed = False
        self._top = None
        self._sub_blocks_order = None
        self._sub_blocks = None

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def sub_blocks(self):
        return self._sub_blocks

    @property
    @parsed
    def sub_blocks_order(self):
        return self._sub_blocks_order

    @parsed
    def __getitem__(self, key):
        if key in self._sub_blocks:
            return self._sub_blocks[key]
        if type(key) == int:
            index = int(key)
            lang = self.sub_blocks_order[index]
            return self._sub_blocks[lang]
        # if key in self.headers:
        #     return Lan

    @parsed
    def __getattr__(self, key):
        if key in self._sub_blocks:
            return self._sub_blocks[key]

    @parsing
    def _parse(self):
        parts = P.forth_header.split(self.content)
        if len(parts) == 1:
            self._sub_blocks_order = ['']
            self._sub_blocks = {
                '': SubBlockSection(self, '', '', parts[0]),
            }
            return
        self._top = parts.pop(0)
        self._sub_blocks_order = list()
        self._sub_blocks = dict()
        for header, value, content in chunks(parts, 3):
            self._sub_blocks_order.append(value)
            if value in self._sub_blocks:
                raise Exception(f'Duplicated sub-block on the page '
                                f'"{self.title}"')
            self._sub_blocks[value] = \
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
# todo: .. return Special ListObject here with different options: only list, or hierarchy list, etc.
# todo: split this file into smaller files with each class it them
