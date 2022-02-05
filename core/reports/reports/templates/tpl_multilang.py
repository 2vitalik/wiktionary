from pprint import pprint

from shared_utils.wiktionary.wikicode import nowiki_code

from core.reports.lib.complex_report.base import BaseComplexReport
from core.reports.lib.details_sublist.sub_lists import SubLists
from core.reports.lib.mixins.key_title import KeyTitle
from libs.parse.storage_page import StoragePage
from libs.utils.classes import derive


class MultilangTemplate(BaseComplexReport):
    base_path = 'Ошибки/Средние/Шаблоны/multilang'
    base_class = derive(KeyTitle, SubLists)

    report_keys = [
        'Не хватает шаблона',
        'Шаблон лишний',
        'Пустое количество языков',
        'Нерпавильное количество языков',
        'Несколько шаблонов в одной статье',
    ]

    def description(self, report_key):
        descriptions = {
            'Не хватает шаблона': '''
                В статье несколько языковых секций, но нет шаблона 
                {{шаблон|multilang}}.
            ''',
            'Шаблон лишний': '''
                В статье только одна языковая секция, поэтому шаблон
                {{шаблон|multilang}} не нужен. 
            ''',
            'Пустое количество языков': '''
                В шаблоне {{шаблон|multilang}} не указано количество языков.
            ''',
            'Нерпавильное количество языков': '''
                В шаблоне {{шаблон|multilang}} не указано неправильное 
                количество языков.
            ''',
            'Несколько шаблонов в одной статье': '''
                В статье используется несколько шаблонов {{шаблон|multilang}}
                (а должен быть только один).
            ''',
        }
        return descriptions[report_key]

    def fill_values(self, report_key, page, tpls, suffix=''):
        values = []
        for tpl in tpls:
            tpl_content = nowiki_code(tpl.content)
            values.append(f'{tpl_content}{suffix}')
        self.set(report_key, page.title, values)

    def update_page(self, page):
        num_from_page = len(page.keys)

        tpls = list(page.templates('multilang').last_list())
        num_tpls = len(tpls)

        if num_tpls > 1:
            self.fill_values('Несколько шаблонов в одной статье', page, tpls)
            return

        if num_from_page == 1 and num_tpls:
            self.fill_values('Шаблон лишний', page, tpls)
            return

        if num_from_page > 1 and not num_tpls:
            self.fill_values('Не хватает шаблона', page, tpls)
            return

        if not num_tpls:
            return

        params = tpls[0].params.replace(u'|', '').strip()
        if not params:
            self.fill_values('Пустое количество языков', page, tpls)
            return

        num_from_tpl = int(params)
        if num_from_tpl != num_from_page:
            self.fill_values('Нерпавильное количество языков', page, tpls,
                             f" → '''{num_from_page}'''")
            return


if __name__ == '__main__':
    # page = StoragePage('Бергман')
    # page = StoragePage('Estocolmo')
    page = StoragePage('аритметика')
    r = MultilangTemplate()
    r.update_page(page)
    pprint(r.entries)
