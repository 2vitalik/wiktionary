from libs.parse.data.blocks.detailed.base import BaseDetailedData
from libs.parse.utils.decorators import parsing


class VerbData(BaseDetailedData):
    tpls_no_index = [
        'гл ru',
        'гл ru СВ',
        'гл ru НСВ',
        'гл ru НВ',
        'гл ru -ся',
        'гл ru -сяСВ',
        'гл ru -сяНСВ',
    ]

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
    def get_aspect(cls, template):
        if 'НСВ' in template.name:
            return 'несов'
        elif 'СВ' in template.name:
            return 'сов'
        else:
            has_index = cls.check_index(template)
            return "несов" if has_index else None

    @classmethod
    def check_index(cls, template):
        return template.name not in cls.tpls_no_index

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
        has_perfective = None
        has_imperfective = None
        is_perfective_only = None
        is_imperfective_only = None
        has_index = None
        for template in self.base.templates(re='гл*').last_list():
            index = self.get_index(template)  # todo: skip -ся, -сяСВ и т.п.

            if self.check_index(template):
                has_index = True

            impersonal = self.get_impersonal(template)
            if impersonal:
                has_impersonal = True
                if is_impersonal is None:
                    is_impersonal = True
            else:
                is_impersonal = False

            aspect = self.get_aspect(template)
            if aspect == 'сов':
                has_perfective = True
                is_imperfective_only = False
                if is_perfective_only is None:
                    is_perfective_only = True
            elif aspect == 'несов':
                has_imperfective = True
                is_perfective_only = False
                if is_imperfective_only is None:
                    is_imperfective_only = True

            indexes.append(index)

        self._sub_data['indexes'] = indexes
        self._sub_data['has_index'] = has_index
        self._sub_data['is_impersonal'] = is_impersonal
        self._sub_data['has_impersonal'] = has_impersonal
        self._sub_data['has_perfective'] = has_perfective
        self._sub_data['has_imperfective'] = has_imperfective
        self._sub_data['is_perfective_only'] = is_perfective_only
        self._sub_data['is_imperfective_only'] = is_imperfective_only


# todo: проверить, почему сломался "ять" на "check_index"
