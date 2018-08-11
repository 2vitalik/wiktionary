from projects.reports.lib.builders.simple_report import SimpleReportBuilder


class DuplicatedFirstLevel(SimpleReportBuilder):
    path = 'Ошибки/Важные/Заголовки/Первый уровень/Дублирование'
    desc = 'Дубли первого уровня'

    entries = [
        '# просто для примера\n',
        '# да-да\n'
    ]

    def check_bool(self, page) -> bool:
        pass
