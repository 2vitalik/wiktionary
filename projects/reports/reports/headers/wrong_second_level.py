from libs.parse.patterns import TR
from projects.reports.lib.checkers.single.dict_of_lists import DictOfListsReport
from projects.reports.lib.reports.dict_report.dict_of_lists.colon import Colon
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.key_title import \
    KeyTitle
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.value_code import \
    ValueCode


class WrongSecondLevel(Colon, KeyTitle, ValueCode, DictOfListsReport):
    path = 'Ошибки/Важные/Заголовки/Второй уровень/Неправильный'
    description = '''
        Случаи неправильного использования заголовка второго уровня для статей.
        
        Правильным считается заполненный шаблон 
        <code><nowiki>{{з|...}}</nowiki></code> 
        или <code><nowiki>{{заголовок|...}}</nowiki></code>.
    '''

    def check_list(self, page) -> list:
        values = []
        for homonym_obj in page.homonyms.values():
            header = homonym_obj.header
            if not header:
                continue
            if not TR.homonym_header.match(header):
                # print(page.title)
                # print(header)
                # return True
                values.append(header)
        return values
