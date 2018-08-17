from core.storage.main import storage
from libs.utils.classes import derive
from libs.utils.wikicode import bold
from projects.reports.lib.complex_report.base import BaseComplexReport
from projects.reports.lib.details_sublist.brackets import \
    Brackets
from projects.reports.lib.mixins.key_title import KeyTitle
from projects.reports.lib.mixins.value_title import \
    ValueTitle


class VerbsWithoutParticiples(BaseComplexReport):
    base_path = 'Отчёты/ru/Глаголы/Без созданных деепричастий'
    base_class = derive(KeyTitle, ValueTitle, Brackets)

    report_keys = [
        '-ать', # '-аться',
        # '-еть', # '-еться',
        '-ить', # '-иться',
        '-оть', # '-оться',
        '-уть', # '-уться',
        '-ыть', # '-ыться',
        '-ять', # '-яться',
    ]

    def description(self, report_key):
        return f'''
            Глаголы на "{bold(report_key)}" без созданных статей-деепричастий, 
            при этом пока учитывается только факт создания статьи, но не её 
            содержимое.
        '''

    def process_page(self, page):
        for report_key in self.report_keys:
            if page.title.endswith(report_key[1:]):
                if '{{гл ru' not in page.ru.content:
                    continue
                stem = page.title[:-2]
                partitives = [f'{stem}в', f'{stem}вши']
                values = []
                for partitive in partitives:
                    if partitive not in storage.titles_set:
                        values.append(partitive)
                self.set(report_key, page.title, values)


# todo: дополнительно проверять (возможно, для других подотчётов):
# todo:   - страница-редирект, а не полноценная статья
# todo:   - страница есть, но нет омонима-деепричастия
# todo:   - деепричастие есть, но только в виде словоформы
