from libs.parse.data.base import BaseData
from libs.parse.data.language import LanguageData
from libs.parse.utils.decorators import parsing


class PageData(BaseData):

    @property
    def languages(self):
        return self.sub_data.items()

    @parsing
    def _parse(self):
        self._sub_data = {}
        for lang, lang_section in self.base.sub_sections.items():
            self._sub_data[lang] = \
                LanguageData(lang_section, None, self.page, lang)

    @property
    def parsed_data(self):
        data = {}

        warnings = {
            # https://ru.wiktionary.org/wiki/Категория:Викисловарь:Шаблоны:Быстрое_удаление
            'wikify': [
                '{{wikify',
            ],
            'editing': [
                '{{пишу',
            ],
            'to-delete': [
                '{{к удалению', '{{db-', '{{уд-', '{{NCT', '{{hangon',
                '{{orphaned-fairuse',
            ],
        }
        data['base'] = {'warnings': []}
        for warning, templates in warnings.items():
            for template in templates:
                if template in self.page.content:
                    data['base']['warnings'].append(warning)

        if self.page.is_redirect:
            data['base']['redirect'] = True
            return data

        if ' ' in self.page.title:
            data['base']['type'] = 'phrase'
            return data

        if self.page.title.startswith('*'):
            data['base']['type'] = 'proto-slavic'
            return data

        if self.page.title.startswith('-') or self.page.title.endswith('-'):
            data['base']['type'] = 'morpheme'
            return data

        for lang, language in self.page.data.languages:
            data[lang] = language.parsed_data

        return data
