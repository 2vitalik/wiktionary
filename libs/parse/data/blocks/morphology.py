from libs.parse.data.blocks.base import BaseBlockData
# from libs.parse.data.blocks.detailed.morphology.morpho import MorphoData
from libs.parse.data.blocks.detailed.morphology.noun import NounData
from libs.parse.data.blocks.detailed.morphology.verb import VerbData
from libs.parse.utils.decorators import parsing, parsed


class MorphologyData(BaseBlockData):
    @parsed
    def is_verb(self):
        return self.word_type == 'verb'

    @parsed
    def is_noun(self):
        return self.word_type == 'noun'

    def _parse_word_type(self):
        word_type = 'unknown'
        if '{{гл' in self.base.content:
            word_type = 'verb'
        elif '{{сущ' in self.base.content:
            word_type = 'noun'
        return word_type

    @parsing
    def _parse(self):
        word_type = self._parse_word_type()
        self._sub_data = {
            'word_type': word_type,
            'syllables': self.base.templates('по-слогам', 'по-слогам').last_list(),
        }
        if word_type == 'verb':
            self._sub_data['verb'] = VerbData(self.base, self, self.page)
        elif word_type == 'noun':
            self._sub_data['noun'] = NounData(self.base, self, self.page)


# todo: special test-checker: пройтись по категориям "Существительные" и проверять, соответствует ли мой ответ
