from projects.reports.lib.checkers.base import BaseChecker


class SeveralReports(BaseChecker):
    base_path = None
    base_class = None

    reports = {}
    report_keys = None

    def __init__(self):
        self.create_reports()

    def description(self, report_key):
        raise NotImplementedError()

    def create_reports(self):
        for report_key in self.report_keys:
            path = f'{self.base_path}/{report_key}'
            description = self.description(report_key)
            self.reports[report_key] = self.base_class(path, description)

    def check(self, page):
        raise NotImplementedError()

    def build(self) -> list:
        return list(self.reports.values())
