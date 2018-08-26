from libs.parse.data.base import BaseData
from libs.parse.data.blocks.chooser import BlockData
from libs.parse.utils.decorators import parsing


class HomonymData(BaseData):

    @parsing
    def _parse(self):
        self._sub_data = {}
        for block_key, block_section in self.base.sub_sections.items():
            block_data_class = BlockData.get_class(block_key)
            self._sub_data[block_key] = block_data_class(block_section)
