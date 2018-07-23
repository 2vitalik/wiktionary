from lib.parse.sections.base import BaseSection
from lib.parse.utils.decorators import parsing


class SubBlockSection(BaseSection):
    is_leaf = True

    @parsing
    def _parse(self):
        self._sub_sections = dict()
