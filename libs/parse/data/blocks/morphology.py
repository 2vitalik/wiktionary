from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.data.blocks.detailed.verb import VerbData
from libs.parse.utils.decorators import parsing


class MorphologyData(BaseBlockData):

    def parse_word_type(self):
        word_type = 'unknown'
        if '{{гл' in self.base.content:
            word_type = 'verb'
        elif '{{сущ' in self.base.content:
            word_type = 'noun'
        return word_type

    @parsing
    def _parse(self):
        word_type = self.parse_word_type()
        self._sub_data = {
            'word_type': word_type,
            'syllables': self.base.templates('по-слогам', 'по-слогам').last_list(),
        }
        if word_type == 'verb':
            self._sub_data['verb'] = VerbData(self.base)
