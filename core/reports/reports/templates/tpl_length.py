import re
from pprint import pprint

from shared_utils.wiktionary.wikicode import nowiki_code

from core.reports.lib.complex_report.base import BaseComplexReport
from core.reports.lib.details_sublist.sub_lists import SubLists
from core.reports.lib.mixins.key_title import KeyTitle
from libs.parse.storage_page import StoragePage
from libs.utils.classes import derive


class WrongLength(BaseComplexReport):
    def __init__(self):
        super().__init__()
        self.base_path = 'Ошибки/Средние/Шаблоны/Длина слова'
        self.base_class = derive(KeyTitle, SubLists)

        self.report_keys = [
            'Нестандартное расположение параметров',
            'Не в той языковой секции',
            'Неверный язык (секции нет)',
            'Неверная длина',
            'В статьях с пробелами',
        ]
        self.create_reports()

    def description(self, report_key):
        descriptions = {
            'Нестандартное расположение параметров': '''
                Необычное расположение параметров в шаблоне 
                {{шаблон|длина слова}}, обычно идёт длина, а потом код языка.
            ''',
            'Не в той языковой секции': '''
                Шаблон {{шаблон|длина слова}} находится не в той языковой 
                секции.
            ''',
            'Неверный язык (секции нет)': '''
                Язык шаблона {{шаблон|длина слова}} не совпадает ни с одной 
                языковой секцией в статье.
            ''',
            'Неверная длина': '''
                Указана неправильная длина в шаблоне {{шаблон|длина слова}}.
            ''',
            'В статьях с пробелами': '''
                Случаи использование шаблона в статьях с пробелами
            ''',
        }
        return descriptions[report_key]

    def update_page(self, page):
        values = {
            'Нестандартное расположение параметров': [],
            'Не в той языковой секции': [],
            'Неверный язык (секции нет)': [],
            'Неверная длина': [],
            'В статьях с пробелами': [],
        }

        length_fom_page = len(page.title.replace('-', ''))

        for lang_from_page, template in page.templates('длина слова'):
            if not lang_from_page:
                lang_from_page = '???'

            tpl_content = nowiki_code(template.content)

            if ' ' in page.title:
                values['В статьях с пробелами'].append(
                    f'{lang_from_page}: {tpl_content}'
                )

            m = re.fullmatch(r'^(?P<len>\d+)\|(?:lang=)?(?P<lang>[^=|}]+)$',
                             template.params)
            if not m:
                values['Нестандартное расположение параметров'].append(
                    f'{lang_from_page}: {tpl_content}'
                )
                continue

            # Берём данные из шаблона:
            lang_from_tpl = m.group(2)
            length_from_tpl = int(m.group(1))

            # Проверяем язык:
            if lang_from_tpl != lang_from_page:
                if lang_from_tpl in page.keys:
                    values['Не в той языковой секции'].append(
                        f'{lang_from_page}: {tpl_content} → {lang_from_tpl}'
                    )
                else:
                    values['Неверный язык (секции нет)'].append(
                        f'{lang_from_page}: {tpl_content}'
                    )

            # Проверяем длину:
            if length_from_tpl != length_fom_page:
                values['Неверная длина'].append(
                    f'{lang_from_page}: {tpl_content} → {length_fom_page}'
                )

        for report_key, value in values.items():
            self.set(report_key, page.title, value)


if __name__ == '__main__':
    page = StoragePage('Pashtun')
    r = WrongLength()
    r.update_page(page)
    pprint(r.entries)
