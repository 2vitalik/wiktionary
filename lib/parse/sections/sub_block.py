from lib.parse.patterns import H
from lib.parse.sections.base import BaseSection
from lib.parse.utils.decorators import parsing


class SubBlockSection(BaseSection):
    is_leaf = True

    def __init__(self, base, full_header, header, content):
        super().__init__(base, full_header, header, content)
        self._key = H.get_key(header)

    @parsing
    def _parse(self):
        self._sub_sections = dict()
