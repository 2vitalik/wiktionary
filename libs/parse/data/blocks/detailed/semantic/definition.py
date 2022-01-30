import re

from libs.parse.data.blocks.detailed.semantic.base import BaseSemanticData
from libs.parse.utils.decorators import parsing


class DefinitionData(BaseSemanticData):
    def check_examples(self, value):
        value = re.sub('{{\s*пример[|\s]*(\|[^|=}]+=)*[|\s]*\}\}', '', value)
        return re.search('{{\s*пример', value, re.UNICODE)

    @parsing
    def _parse(self):
        proto = None
        files = []
        values = []
        has_examples = False
        need_more_examples = False

        for line in self.get_entries():
            if self.check_empty(line):
                continue
            if re.match('^\[\[(Файл:|File:|Image:|Изображение:).+\]\]$', line,
                        re.UNICODE):
                files.append(line)
                continue
            if line.startswith('{{прото'):
                if proto:
                    ...  # todo: error
                proto = line
                continue
            if not line.startswith('#'):
                ...  # todo: error

            if self.check_examples(line):
                has_examples = True
            else:
                need_more_examples = True

            values.append(line)

        self._sub_data = {
            'proto': proto,
            'files': files,
            'values': values,
            'has_examples': has_examples,
            'need_more_examples': need_more_examples,
        }
