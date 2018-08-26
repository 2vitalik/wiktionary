from libs.parse.data.blocks.detailed.base import BaseDetailedData
from libs.parse.utils.decorators import parsing


class VerbData(BaseDetailedData):

    @classmethod
    def get_impersonal(cls, template):
        if '|безличный=1' in template.params:
            return True
        impersonal_templates = [
            'гл ru 4b-ш-безл',
            'гл ru 4a-ь-безл-ся',
            'гл ru 5b/c"-ся',
        ]
        if template.name in impersonal_templates:
            return True
        return False

    @classmethod
    def get_index(cls, template):
        index = template.name
        if index.startswith('гл ru '):
            index = index[len('гл ru '):]
        return index

    @parsing
    def _parse(self):
        self._sub_data = {}
        indexes = []
        is_impersonal = None
        has_impersonal = None
        for template in self.base.templates(re='гл*').values():
            index = self.get_index(template)

            impersonal = self.get_impersonal(template)
            if impersonal:
                has_impersonal = True
                if is_impersonal is None:
                    is_impersonal = True
            else:
                is_impersonal = False

            indexes.append(index)
        self._sub_data['indexes'] = indexes
        self._sub_data['is_impersonal'] = is_impersonal
        self._sub_data['has_impersonal'] = has_impersonal
