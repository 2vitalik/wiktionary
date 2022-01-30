from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.data.blocks.chooser import BlockData
from libs.parse.data.blocks.detailed.semantic.top import SemanticTopData
from libs.parse.utils.decorators import parsing


class SemanticData(BaseBlockData):
    @parsing
    def _parse(self):
        self._sub_data = {
            'top': SemanticTopData(self.base, self, self.page),
        }
        for block_key, block_section in self.base.sub_sections.items():
            block_data_class = BlockData.get_class(block_key)
            self._sub_data[block_key] = \
                block_data_class(block_section, self, self.page)

    @property
    def parsed_data(self):
        if self.base.templates('значение'):
            return {'todo'}  # fixme
        if self.base.templates('семантика'):
            return {'todo'}  # fixme

        data = {
            'top': self['top'].parsed_data,
        }
        headers = [
            'definition', 'synonyms', 'antonyms', 'hyperonyms', 'hyponyms',
        ]
        for header in headers:
            if header not in self.sub_data:
                data[header] = {'header': False}
            else:
                data[header] = self[header].parsed_data
        return data
