from libs.parse.data.blocks.detailed.semantic.base import BaseSemanticData
from libs.parse.utils.decorators import parsing


class BaseOnymsData(BaseSemanticData):
    @parsing
    def _parse(self):
        values = []
        for line in self.get_entries():
            if not line.strip():
                continue
            values.append(line)

        self._sub_data = {
            'value': values,
        }
