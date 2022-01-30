import re

from core.reports.lib.details_sublist.sub_lists import SubLists
from core.reports.lib.mixins.key_title import KeyTitle
from libs.parse.storage_page import StoragePage


class WrongLength(KeyTitle, SubLists):  # todo: remove (see tpl_length.py)
    path = 'Ошибки/Средние/Шаблоны/Длина слова/Неверная длина'
    description = '''
        Указана неправильная длина в шаблоне {{шаблон|длина слова}}
    '''

    def check_page(self, page) -> list:
        values = []
        for lang, template in page.templates('длина слова'):
            m = re.match('^(\d+)', template.params)
            if m:
                length_from_tpl = int(m.group(1))
                length_fom_title = len(page.title.replace('-', ''))
                if length_from_tpl != length_fom_title:
                    values.append(
                        f'{lang}: '
                        f'<code><nowiki>{template.content}</nowiki></code> '
                        f'→ {length_fom_title}'
                    )
        return values


if __name__ == '__main__':
    page = StoragePage('сало')
    WrongLength().check_page(page)
