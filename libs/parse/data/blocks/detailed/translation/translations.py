import re

from libs.parse.data.blocks.detailed.base import BaseDetailedData
from libs.parse.utils.decorators import parsing


class TranslationsData(BaseDetailedData):
    @parsing
    def _parse(self):
        templates = []
        print()
        for key, tpl in self.base.templates('перев-блок'):
            values = {
                key: re.sub('<!--.*?-->', '', value).strip()
                for key, value in tpl.kwargs.items()
            }
            values = {
                key: value for key, value in values.items() if value
            }
            t = {
                'name': tpl.name,
                'title': tpl.args[0].strip(),
                'values': values,
                'has_data': bool(values),
                'wrong': [],
            }
            templates.append(t)

        self._sub_data = {
            'has_data': sum([t['has_data'] for t in templates]),
            'templates': templates,
        }
