from libs.parse.patterns import TR
from libs.utils.collection import chunks
from projects.reports.lib.checkers.single.dict_of_lists import DictOfListsReport
from projects.reports.lib.reports.dict_report.dict_of_lists.brackets import \
    Brackets
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.key_title import \
    KeyTitle
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.value_code import \
    ValueCode


class DuplicatedFirstLevel(Brackets, KeyTitle, ValueCode, DictOfListsReport):
    path = 'Ошибки/Важные/Заголовки/Первый уровень/Дублирование'
    description = '''
        Дубли заголовков первого уровня
    '''

    def check_list(self, page) -> list:
        values = []
        parts = TR.lang_header.split(self.content)
        headers = set()
        if len(parts) == 1:
            return []  # наверное, редирект
        parts.pop(0)
        for full_header, header, content in chunks(parts, 3):
            if header in headers:
                values.append(header)
            headers.add(header)
        return values
