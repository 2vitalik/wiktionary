from libs.parse.patterns import TR
from projects.reports.lib.checkers.single.dict_of_lists import DictOfListsReport
from projects.reports.lib.reports.dict_report.dict_of_lists.colon import Colon
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.key_title import \
    KeyTitle
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.value_code import \
    ValueCode


class WrongFirstLevel(Colon, KeyTitle, ValueCode, DictOfListsReport):
    path = 'Ошибки/Важные/Заголовки/Первый уровень/Неправильный'
    description = '''
        Случаи неправильного использования заголовка первого уровня для статей.
        
        Правильным считается формат <code><nowiki>{{-lang-}}</nowiki></code> 
        или <code><nowiki>{{-lang-|...}}</nowiki></code>,
        где <code><nowiki>lang</nowiki></code> — код языка, 
        который не содержит лишние невидимые символы.
    '''

    def check_list(self, page) -> list:
        values = []
        for language_obj in page.languages.values():
            header = language_obj.header
            if not header:  # возможно, редирект
                continue
            if not TR.lang_header.match(header):
                print(page.title)
                print(header)
                values.append(header)
        return values
