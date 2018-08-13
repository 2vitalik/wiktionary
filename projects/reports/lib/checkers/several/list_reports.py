from projects.reports.lib.checkers.several.base import SeveralReports


class SeveralListReports(SeveralReports):
    def description(self, key):
        raise NotImplementedError()

    def check(self, page):
        raise NotImplementedError()

    def add(self, report_key, *args):
        self.reports[report_key].add(*args)
