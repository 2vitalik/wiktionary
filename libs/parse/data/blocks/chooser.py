from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.data.blocks.etymology import EtymologyData
from libs.parse.data.blocks.morphology import MorphologyData
from libs.parse.data.blocks.phrases import PhrasesData
from libs.parse.data.blocks.pronunciation import PronunciationData
from libs.parse.data.blocks.related_words import RelatedWordsData
from libs.parse.data.blocks.semantic import SemanticData
from libs.parse.data.blocks.translate import TranslateData


class BlockData:
    classes = {
        'morphology': MorphologyData,
        'pronunciation': PronunciationData,
        'semantic': SemanticData,
        # 'definition': DefinitionData,
        # 'synonyms': SynonymsData,
        # 'antonyms': AntonymsData,
        # 'hyperonyms': HyperonymsData,
        # 'hyponyms': HyponymsData,
        'related_words': RelatedWordsData,
        'etymology': EtymologyData,
        'phrases': PhrasesData,
        'translate': TranslateData,
        # 'bibliography': BibliographyData,

    }

    @classmethod
    def get_class(cls, block_key):
        return cls.classes.get(block_key, BaseBlockData)
