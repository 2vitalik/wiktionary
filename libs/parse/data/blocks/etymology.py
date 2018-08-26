from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.utils.decorators import parsing, parsed


class EtymologyData(BaseBlockData):
    @property
    @parsed
    def has_data(self):
        return  # todo

    @parsing
    def _parse(self):
        pass  # todo
