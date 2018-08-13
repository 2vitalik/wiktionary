from core.storage.main import MainStorage, storage
from libs.utils.classes import derive
from libs.utils.wikicode import bold
from projects.reports.lib.checkers.several.list_reports import \
    SeveralListReports
from projects.reports.lib.reports.dict_report.dict_of_lists.brackets import \
    Brackets
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.key_title import \
    KeyTitle
from projects.reports.lib.reports.dict_report.dict_of_lists.mixins.value_title import \
    ValueTitle


class VerbsWithoutParticiples(SeveralListReports):
    base_path = 'Отчёты/ru/Глаголы/Без созданных деепричастий'
    base_class = derive(KeyTitle, ValueTitle, Brackets)

    report_keys = [
        '-ать', # '-аться',
        # '-еть', # '-еться',
        '-оть', # '-оться',
        '-уть', # '-уться',
        '-ыть', # '-ыться',
        '-ять', # '-яться',
    ]

    def __init__(self):  # todo: move this in somewhere common place for all reports
        super().__init__()
        self.titles = set(storage.titles)

    def description(self, report_key):
        return f'''
            Глаголы на "{bold(report_key)}" без созданных статей-деепричастий, 
            при этом пока учитывается только факт создания статьи, но не её 
            содержимое.
        '''

    def check(self, page):
        for report_key in self.report_keys:
            if page.title.endswith(report_key[1:]):
                if '{{гл ru' not in page.ru.content:
                    continue
                stem = page.title[:-2]
                partitives = [f'{stem}в', f'{stem}вши']
                for partitive in partitives:
                    if partitive not in self.titles:
                        self.add(report_key, page.title, partitive)


# todo: дополнительно проверять (возможно, для других подотчётов):
# todo:   - страница-редирект, а не полноценная статья
# todo:   - страница есть, но нет омонима-деепричастия
# todo:   - деепричастие есть, но только в виде словоформы
