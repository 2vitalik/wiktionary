from libs.parse.data.base import BaseData
from libs.parse.data.homonym import HomonymData
from libs.parse.utils.decorators import parsing


class LanguageData(BaseData):

    @parsing
    def _parse(self):
        for homonym_key, homonym_section in self.base.sub_sections.items():
            self._sub_data[homonym_key] = HomonymData(homonym_section)

    def is_verb(self):
        raise NotImplementedError()  # todo

    def has_noun(self):
        for homonym in self:
            m = homonym.morphology
            if m and m.word_type == 'noun':
                return True
        return False

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
            if m and m.is_verb() and m.verb.has_impersonal:
                return True
        return False

    def has_indexed_noun(self):
        for homonym in self:
            m = homonym.morphology
            if m and m.is_noun() and m.noun.has_index:
                return True
        return False

    def has_indexed_verb(self):
        for homonym in self:
            m = homonym.morphology
            if m and m.is_verb() and m.verb.has_index:
                return True
        return False

    def has_unindexed_verb(self):
        for homonym in self:
            m = homonym.morphology
            if m and m.is_verb() and not m.verb.has_index:
                return True
        return False

    def has_untranscribed_verb(self):
        for homonym in self:
            m = homonym.morphology
            p = homonym.pronunciation
            if m and m.is_verb() and not p.transcriptions.has_data:
                return True
        return False
