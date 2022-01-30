from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.utils.decorators import parsing


class SemanticTopData(BaseBlockData):
    @parsing
    def _parse(self):
        self._sub_data = {}
        ...

    def base_parsed_data(self):
        return {
            'header': True,
            'has_content': self.base.top.strip() != '',
        }
