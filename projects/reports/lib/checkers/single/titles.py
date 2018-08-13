from projects.reports.lib.checkers.single.base import BaseSingleChecker
from projects.reports.lib.reports.list_report.list_of_titles.simple import \
    TitlesList


class TitlesReport(TitlesList, BaseSingleChecker):
    def check(self, page):
        if self.check_bool(page):
            self.add(page.title)

    def check_bool(self, page) -> bool:
        raise NotImplementedError()
