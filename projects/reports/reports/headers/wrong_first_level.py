from libs.parse.patterns import TR
from projects.reports.lib.builders.simple_report import SimpleReportBuilder


class WrongFirstLevel(SimpleReportBuilder):
    path = 'Ошибки/Важные/Заголовки/Первый уровень/Неправильный'
    desc = 'Неправильные первые уровни'

    def check_bool(self, page) -> bool:
        for language_obj in page.languages.values():
            header = language_obj.header
            if not header:  # возможно, редирект
                continue
            if not TR.lang_header.match(header):
                print(page.title)
                print(header)
                return True
