from __future__ import annotations

from typing import Dict

from libs.parse.groupers.sections.base import BaseSectionsGrouper
from libs.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from libs.parse.groupers.sections.empty import EmptyBaseSectionsGrouper
from libs.parse.patterns import H
from libs.parse.utils.decorators import parsed, parsing
from libs.utils.collection import chunks


class BaseSection(BaseSectionsGrouper):
    is_leaf: bool = False
    parse_pattern = None
    child_section_type = None
    copy_top_to_sub_sections: bool = False

    def __init__(self, base: str, full_header: str, header: str, content: str, silent: bool):
        super().__init__(base)

        # leafs don't have sub-sections don't parse anything
        if not self.is_leaf:
            if not self.parse_pattern:
                raise NotImplementedError('`parse_pattern` is absent')
            if not self.child_section_type:
                raise NotImplementedError('`child_section_type` is absent')

        self.base = base
        if base:
            self.title: str = base.title
            """The page title"""
        self.full_header: str = full_header
        self.header: str = header
        self.content: str = content
        self.silent: bool = silent

        self.is_parsing: bool = False
        self.parsed: bool = False
        self._key = None
        self._top: str = None
        self._sub_sections: Dict[str, BaseSection] = None  # TODO: fix None
        self._old_content: str = content
        """The string that contains content of Section before any changes made"""

    def __str__(self):
        name = type(self).__name__
        return f"{name}('{self.key}')"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.full_header == other.full_header and \
               self.header == other.header and self.content == other.content

    def __bool__(self):
        return True  # т.к. этот элемент всегда "есть"

    @property
    def key(self) -> str:
        if self._key is not None:
            return self._key
        if self.header is not None:
            return self.header
        return self.title

    @property
    @parsed
    def top(self):
        """Returns the text between section's header but before the first sub-section.
        So, for example, for Page this would be text of section 0.
        TODO rename to more meaningful title"""
        return self._top

    @property
    @parsed
    def sub_sections(self) -> Dict[str, BaseSection]:
        return self._sub_sections

    @property
    @parsed
    def keys(self):
        """All children sections keys
        TODO rename to more meaningful title"""
        return list(self._sub_sections.keys())

    @parsed
    def __getitem__(self, index):
        # Непосредственное обращение к дочернему элементу?
        if index in self.sub_sections:
            return self.sub_sections[index]

        # Обращение по числовому индексу?
        if type(index) == int:
            key = list(self.sub_sections.keys())[int(index)]
            return self.sub_sections[key]

        # Обращение по стандартному заголовку?
        header_key = H.get_key(index)
        if header_key:
            if header_key in self.sub_sections:
                return self.sub_sections[header_key]
            else:
                return AnyBlocksGrouper(self, header_key)

        # Обращение по ключу заголовка?
        if index in H.headers.keys():
            return AnyBlocksGrouper(self, index)

        # По умолчанию пытаемся сгруппировать по неизвестному заголовку:
        return AnyBlocksGrouper(self, index)

    @parsed
    def __getattr__(self, attr):
        if attr in self.sub_sections:
            return self.sub_sections[attr]
        if attr in H.headers:
            return AnyBlocksGrouper(self, attr)
        return EmptyBaseSectionsGrouper(self)

    @parsed
    def __iter__(self):
        for key, section in self.sub_sections.items():
            yield key, section

    @parsing
    def _parse(self):
        parts = self.parse_pattern.split(self.content)
        if len(parts) == 1:
            self._top = ''
            self._sub_sections = {
                '': self.child_section_type(self, '', '', parts[0],
                                            self.silent),
            }
            return
        self._top = parts.pop(0)
        self._sub_sections = dict()
        if self.copy_top_to_sub_sections:
            self._sub_sections[''] = \
                self.child_section_type(self, '', '', self._top, self.silent)
        for full_header, header, content in chunks(parts, 3):
            if header in self._sub_sections and not self.silent:
                raise Exception(f'Duplicated section `{header}` on the page '
                                f'"{self.title}"')
            child_section = \
                self.child_section_type(self, full_header, header, content,
                                        self.silent)
            key = child_section.key
            if key in self._sub_sections and not self.silent:
                raise Exception(f'Duplicated header key `{key}` on the page '
                                f'"{self.title}"')
            self._sub_sections[key] = child_section

    def sub_sections_content(self):
        if self._sub_sections is None:
            return
        content = self.top
        for key, section in self.sub_sections.items():
            content += section.new_content
        return content

    @property
    def new_content(self):
        sub_sections_content = self.sub_sections_content()
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
