from lib.parse.utils.decorators import parsed, parsing
from lib.utils.collection import chunks


class BaseSection:
    is_leaf = False
    parse_pattern = None
    child_section_type = None

    def __init__(self, base, full_header, header, content):
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
