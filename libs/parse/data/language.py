from libs.parse.data.base import BaseData
from libs.parse.data.homonym import HomonymData
from libs.parse.utils.decorators import parsing


class LanguageData(BaseData):

    @parsing
    def _parse(self):
        self._sub_data = {}
        for homonym_key, homonym_section in self.base.sub_sections.items():
            self._sub_data[homonym_key] = HomonymData(homonym_section)

    def is_verb(self):
        raise NotImplementedError()  # todo

    def has_verb(self):
        for homonym in self:
            m = homonym.morphology
            if m and m.word_type == 'verb':
                return True
        return False

    def is_impersonal_verb_only(self):
        result = None
        for homonym in self:
            m = homonym.morphology
            if m and m.word_type == 'verb':
                if not m.verb.is_impersonal:
                    return False
                else:
                    result = True
        return result

    def has_impersonal_verb(self):
        for homonym in self:
            m = homonym.morphology
            if m and m.word_type == 'verb':
                if m.verb.has_impersonal:
                    return True
        return False
