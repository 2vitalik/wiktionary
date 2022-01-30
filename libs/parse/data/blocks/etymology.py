import re

from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.utils.decorators import parsing


class EtymologyData(BaseBlockData):
    def remove_blank(self, value):
        value = value.replace('Происходит от', ''). \
            replace('От', '').replace('??', '').replace('*', ''). \
            replace('#', '').replace('{{этимология:|да}}', '')
        value = re.sub('{{этимология:(\|[-\w]*)?\}\}', '', value)
        value = self.remove_bottom_templates(value)
        return value.strip()

    @parsing
    def _parse(self):
        self._sub_data = {
            'has_data': self.remove_blank(self.base.content) not in ['', '-'],
        }
