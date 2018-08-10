from libs.parse.patterns import H
from libs.parse.sections.base import BaseSection
from libs.parse.utils.decorators import parsing


class SubBlockSection(BaseSection):
    is_leaf = True

    def __init__(self, base, full_header, header, content, silent):
        super().__init__(base, full_header, header, content, silent)
        self._key = H.get_key(header)

    @parsing
    def _parse(self):
        self._sub_sections = dict()
