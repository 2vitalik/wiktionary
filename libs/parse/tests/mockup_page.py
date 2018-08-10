from libs.parse.patterns import H
from libs.parse.sections.homonym import HomonymSection
from libs.parse.sections.language import LanguageSection
from libs.parse.sections.page import Page


class MockupPage(Page):
    morphology_ru_sample = '''
        {{сущ ru|...}}
        
        {{морфо-ru|...}}
    '''

    morphology_xx_sample = '''
        {{сущ en|...}}

        {{морфо|...}}
    '''

    pronunciation_ru_sample = '''
        {{transcription-ru|...}}
    '''

    pronunciation_xx_sample = '''
        {{transcription|...}}
    '''

    homonym_ru_sample = {
        H.morphology: morphology_ru_sample,
        H.pronunciation: pronunciation_ru_sample,
    }

    homonym_xx_sample = {
        H.morphology: morphology_xx_sample,
        H.pronunciation: pronunciation_xx_sample,
    }

    def __init__(self, title=''):
        self.dict = {
            'ru': {
                '': self.homonym_ru_sample,
            },
            'en': {
                'I': self.homonym_xx_sample,
                'II': self.homonym_xx_sample,
                'III': self.homonym_xx_sample,
            }
        }
        content = self._generate_content(self.dict)
        super().__init__(title, content)
        self._generate_sections_objects()

    def _generate_content(self, data):
        content = ''
        self.lang_sections_args = dict()
        self.homonym_sections_args = dict()
        for lang, lang_dict in data.items():
            lang_header = f'{{{{-{lang}-}}}}'
            lang_full_header = f'= {lang_header} ='
            lang_content = '\n'
            self.homonym_sections_args[lang] = dict()
            for homonym, homonym_dict in lang_dict.items():
                homonym_content = '\n'
                for header, header_content in homonym_dict.items():
                    homonym_content += f'=== {header} ===\n'
                    homonym_content += f'{header_content}\n'

                homonym_content_arg = homonym_content
                if homonym:
                    homonym_header = f'{{{{заголовок|{homonym}}}}}'
                    homonym_full_header = f'== {homonym_header} =='
                else:
                    homonym_header = homonym_full_header = ''
                    # если заголовка нет, то появляется лишний `\n` в парсинге
                    # и его надо учесть для mocked-переменной:
                    homonym_content_arg = '\n' + homonym_content_arg
                self.homonym_sections_args[lang][homonym] = \
                    (homonym_full_header, homonym_header, homonym_content_arg)
                lang_content += f'{homonym_full_header}{homonym_content}'
            self.lang_sections_args[lang] = \
                (lang_full_header, lang_header, lang_content)
            content += f'{lang_full_header}{lang_content}'
        return content

    def _generate_sections_objects(self):
        self.lang_sections = \
            {lang: LanguageSection(self, *args)
             for lang, args in self.lang_sections_args.items()}
        self.homonym_sections = self.homonym_sections_args.copy()
        for lang, homonyms in self.homonym_sections.items():
            for homonym, args in homonyms.items():
                lang_section = self.lang_sections[lang]
                homonyms[homonym] = HomonymSection(lang_section, *args)
