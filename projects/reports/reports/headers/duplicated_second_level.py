from libs.parse.patterns import TR, R
from libs.utils.collection import chunks
from projects.reports.lib.checkers.single.dict_of_lists import DictOfListsReport
from projects.reports.lib.reports.dict_report.dict_of_lists.brackets import \
    Brackets
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.key_title import \
    KeyTitle
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.value_lang_and_code import \
    ValueLangAndCode


class DuplicatedSecondLevel(Brackets, KeyTitle, ValueLangAndCode,
                            DictOfListsReport):
    path = 'Ошибки/Важные/Заголовки/Второй уровень/Дублирование'
    description = '''
        Дубли заголовков второго уровня
    '''

    def check_list(self, page) -> list:
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
