from projects.reports.lib.builders.simple_report import SimpleReportBuilder


class WrongSecondLevel(SimpleReportBuilder):
    path = 'Ошибки/Важные/Заголовки/Второй уровень/Неправильный'
    desc = 'Неправильные вторые уровни'

    def check_bool(self, page) -> bool:
        pass
