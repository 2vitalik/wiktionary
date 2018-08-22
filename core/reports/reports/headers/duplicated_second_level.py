from libs.parse.patterns import R
from libs.utils.collection import chunks
from core.reports.lib.details_sublist.brackets import Brackets
from core.reports.lib.mixins.key_title import KeyTitle
from core.reports.lib.mixins.value_lang_and_code import ValueLangAndCode


class DuplicatedSecondLevel(KeyTitle, ValueLangAndCode, Brackets):
    path = 'Ошибки/Важные/Заголовки/Второй уровень/Дублирование'
    description = '''
        Дубли заголовков второго уровня
    '''

    def check_page(self, page) -> list:
        values = []
        for lang, language_obj in page.languages.items(unique=True).items():
            # print(page.title, lang, language_obj)
            parts = R.second_header.split(language_obj.content)
            if len(parts) == 1:
                continue  # наверное, редирект
            headers = set()
            # print(parts)
            parts.pop(0)
            for full_header, header, content in chunks(parts, 3):
                if header in headers:
                    values.append((lang, header))
                headers.add(header)
        return values
