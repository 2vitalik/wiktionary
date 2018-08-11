from projects.reports.lib.builders.simple_report import SimpleReportBuilder


class VerbsWithoutParticiples(SimpleReportBuilder):
    path = 'Отчёты/ru/Глаголы/Без созданных деепричастий'
    desc = '''
        Глаголы без деепричастий, учитывается только факт создания статьи,
        ... 
    '''

    entries = [
        'пример'
    ]

    def check_bool(self, page) -> bool:
        pass
