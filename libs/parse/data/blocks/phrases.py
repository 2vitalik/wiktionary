from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.utils.decorators import parsing


class PhrasesData(BaseBlockData):
    @parsing
    def _parse(self):
        self._sub_data = {}
