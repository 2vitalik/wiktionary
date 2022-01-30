from libs.parse.data.base import BaseData
from libs.parse.data.blocks.chooser import BlockData
from libs.parse.utils.decorators import parsing


class HomonymData(BaseData):
    @property
    def lang(self):
        return self.base_data.lang

    @property
    def blocks(self):
        return self.sub_data.items()

    @parsing
    def _parse(self):
        self._sub_data = {}
        for block_key, block_section in self.base.sub_sections.items():
            block_data_class = BlockData.get_class(block_key)
            self._sub_data[block_key] = \
                block_data_class(block_section, self, self.page)

    @property
    def parsed_data(self):
        data = {}
        if len(self.blocks) == 1 and '' in self.sub_data:
            data['tags'] = {'form'}  # fixme: скорее всего словоформа?
            return data

        data['tags'] = {'word'}

        headers = ['morphology', 'pronunciation', 'semantic', 'etymology']
        if self.lang == 'ru':
            headers.append('translation')

        for header in headers:
            if header not in self.sub_data:
                data[header] = {'header': False}
            else:
                data[header] = self[header].parsed_data

        return data
