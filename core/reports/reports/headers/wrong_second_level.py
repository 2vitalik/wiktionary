from libs.parse.patterns import TR
from core.reports.lib.details_sublist.colon import Colon
from core.reports.lib.mixins.key_title import KeyTitle
from core.reports.lib.mixins.value_code import ValueCode


class WrongSecondLevel(KeyTitle, ValueCode, Colon):
    path = 'Ошибки/Важные/Заголовки/Второй уровень/Неправильный'
    description = '''
        Случаи неправильного использования заголовка второго уровня для статей.
        
        Правильным считается заполненный шаблон 
        <code><nowiki>{{з|...}}</nowiki></code> 
        или <code><nowiki>{{заголовок|...}}</nowiki></code>.
    '''

    def check_page(self, page) -> list:
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
