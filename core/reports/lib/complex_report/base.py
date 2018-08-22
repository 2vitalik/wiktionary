from core.reports.lib.base import ImportExportMixin


class BaseComplexReport(ImportExportMixin):
    base_path = None
    base_class = None

    reports = {}
    report_keys = None

    def __init__(self):
        self.entries = {}
        self.create_reports()

    def description(self, report_key):
        raise NotImplementedError()

    def process_page(self, page):
        raise NotImplementedError()

    def set(self, report_key, *args):
        self.reports[report_key].set(*args)

    def remove(self, report_key, *args):
        self.reports[report_key].remove(*args)

    def create_reports(self):
        for report_key in self.report_keys:
            path = f'{self.base_path}/{report_key}'
            description = self.description(report_key)
            report = self.base_class(path, description)
            self.reports[report_key] = report
            self.entries[report_key] = report.entries

    def report_pages(self) -> list:
        return list(self.reports.values())

    def convert_entries(self):
        for report_key, report in self.reports.items():
            report.convert_entries()
            self.entries[report_key] = report.entries

    def import_entries(self, suffix=''):
        super().import_entries(suffix)
        for report_key, report in self.reports.items():
            report.entries = self.entries[report_key]
