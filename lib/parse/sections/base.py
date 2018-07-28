from lib.parse.groupers.sections.base import BaseSectionsGrouper
from lib.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from lib.parse.groupers.sections.empty import EmptyBaseSectionsGrouper
from lib.parse.patterns import H
from lib.parse.utils.decorators import parsed, parsing
from lib.utils.collection import chunks


class BaseSection(BaseSectionsGrouper):
    is_leaf = False
    parse_pattern = None
    child_section_type = None

    def __init__(self, base, full_header, header, content):
        super().__init__(base)

        if not self.is_leaf:
            if not self.parse_pattern:
                raise NotImplementedError('`parse_pattern` is absent')
            if not self.child_section_type:
                raise NotImplementedError('`child_section_type` is absent')

        self.base = base
        if base:
            self.title = base.title
        self.full_header = full_header
        self.header = header
        self.content = content

        self.is_parsing = False
        self.parsed = False
        self._key = None
        self._top = None
        self._sub_sections = None
        self._old_content = content

    def __str__(self):
        name = type(self).__name__
        return f'{name}({self.key})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.full_header == other.full_header and \
            self.header == other.header and self.content == other.content

    @property
    def key(self):
        if self._key is not None:
            return self._key
        return self.header

    @property
    @parsed
    def top(self):
        return self._top

    @property
    @parsed
    def sub_sections(self):
        return self._sub_sections

    @property
    @parsed
    def keys(self):
        return list(self._sub_sections.keys())

    @parsed
    def __getitem__(self, index):
        if index in self.sub_sections:
            return self.sub_sections[index]
        if type(index) == int:
            key = list(self.sub_sections.keys())[int(index)]
            return self.sub_sections[key]
        if index in H.headers:
            return AnyBlocksGrouper(self, index)
        key = H.get_key(index)
        if key:
            return AnyBlocksGrouper(self, key)
        return AnyBlocksGrouper(self, index)

    @parsed
    def __getattr__(self, attr):
        if attr in self.sub_sections:
            return self.sub_sections[attr]
        if attr in H.headers:
            return AnyBlocksGrouper(self, attr)
        return EmptyBaseSectionsGrouper()

    @parsed
    def __iter__(self):
        for key, section in self.sub_sections.items():
            yield key, section

    @parsing
    def _parse(self):
        parts = self.parse_pattern.split(self.content)
        if len(parts) == 1:
            self._sub_sections = {
                '': self.child_section_type(self, '', '', parts[0]),
            }
            return
        self._top = parts.pop(0)
        self._sub_sections = dict()
        for full_header, header, content in chunks(parts, 3):
            if header in self._sub_sections:
                raise Exception(f'Duplicated section `{header}` on the page '
                                f'"{self.title}"')
            child_section = \
                self.child_section_type(self, full_header, header, content)
            key = child_section.key
            if key in self._sub_sections:
                raise Exception(f'Duplicated header key `{key}` on the page '
                                f'"{self.title}"')
            self._sub_sections[key] = child_section

    @property
    def sub_sections_content(self):
        if self._sub_sections is None:
            return
        content = self.top
        for key, section in self.sub_sections.items():
            content += section.new_content
        return content

    @property
    def new_content(self):
        sub_sections_content = self.sub_sections_content
        sub_sections_changed = \
            sub_sections_content and sub_sections_content != self._old_content
        field_content_changed = self.content != self._old_content
        if sub_sections_changed and field_content_changed:
            raise Exception('Both contents types was changed, ambiguity.')
        if field_content_changed:
            content = self.content
        elif sub_sections_changed:
            content = sub_sections_content
        else:
            content = self._old_content
        if self.full_header:
            content = f'{self.full_header}{content}'
        return content
