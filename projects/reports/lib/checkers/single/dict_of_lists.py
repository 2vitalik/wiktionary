from projects.reports.lib.checkers.single.base import BaseSingleChecker
from projects.reports.lib.reports.dict_report.dict_of_lists.base import \
    DictOfLists


class DictOfListsReport(DictOfLists, BaseSingleChecker):
    def check(self, page):
        values = self.check_list(page)
        if values:
            self.set(page.title, values)

    def check_list(self, page) -> list:
        raise NotImplementedError()
