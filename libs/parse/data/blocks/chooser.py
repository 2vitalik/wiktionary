from libs.parse.data.blocks.base import BaseBlockData


class BlockData:
    @classmethod
    def get_class(cls, block_key):
        from libs.parse.data.blocks.bibliography import BibliographyData
        from libs.parse.data.blocks.detailed.semantic.definition import \
            DefinitionData
        from libs.parse.data.blocks.detailed.semantic.onyms.antonyms import \
            AntonymsData
        from libs.parse.data.blocks.detailed.semantic.onyms.hyperonyms import \
            HyperonymsData
        from libs.parse.data.blocks.detailed.semantic.onyms.hyponyms import \
            HyponymsData
        from libs.parse.data.blocks.detailed.semantic.onyms.synonyms import \
            SynonymsData
        from libs.parse.data.blocks.etymology import EtymologyData
        from libs.parse.data.blocks.morphology import MorphologyData
        from libs.parse.data.blocks.phrases import PhrasesData
        from libs.parse.data.blocks.pronunciation import PronunciationData
        from libs.parse.data.blocks.related_words import RelatedWordsData
        from libs.parse.data.blocks.semantic import SemanticData
        from libs.parse.data.blocks.translation import TranslationData

        classes = {
            'morphology': MorphologyData,
            'pronunciation': PronunciationData,
            'semantic': SemanticData,
            'definition': DefinitionData,
            'synonyms': SynonymsData,
            'antonyms': AntonymsData,
            'hyperonyms': HyperonymsData,
            'hyponyms': HyponymsData,
            'related_words': RelatedWordsData,
            'etymology': EtymologyData,
            'phrases': PhrasesData,
            'translation': TranslationData,
            'bibliography': BibliographyData,
        }

        return classes.get(block_key, BaseBlockData)
