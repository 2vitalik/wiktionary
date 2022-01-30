from libs.parse.data.base import BaseData
from libs.parse.data.homonym import HomonymData
from libs.parse.utils.decorators import parsing


class LanguageData(BaseData):
    def __init__(self, section, base_data, page, lang):
        self.lang = lang
        super(LanguageData, self).__init__(section, base_data, page)

    @property
    def homonyms(self):
        return self.sub_data.items()

    @parsing
    def _parse(self):
        self._sub_data = {}
        for homonym_key, homonym_section in self.base.sub_sections.items():
            self._sub_data[homonym_key] = \
                HomonymData(homonym_section, self, self.page)

    @property
    def parsed_data(self):
        data = {}
        for homonym_key, homonym in self.homonyms:
            if self.lang == 'Cyrl':
                data[homonym_key] = {'tags': 'letter'}
            else:
                data[homonym_key] = homonym.parsed_data

            # if 'morphology' in homonym.sub_data:
            #     if homonym.morphology.has_content:
            #         d['morphology']['morpho'] = homonym.morphology.morpho.test
            #
            # ...
            #
            # if lang == 'ru' and 'translation' in homonym.sub_data:
            #     ...

        return data

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

    def has_unindexed_noun(self):
        for homonym in self:
            m = homonym.morphology
            if m and m.is_noun() and not m.noun.has_index:
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
