from core.reports.lib.base import ImportExportMixin


class BaseComplexReport(ImportExportMixin):
    def __init__(self):
        self.base_path = None  # should be set in inheritors
        self.base_class = None  # should be set in inheritors
        self.report_keys = None  # should be set in inheritors

        self.reports = {}
        self.entries = {}
        # don't forget to call self.create_reports() in inheritors

    def description(self, report_key):
        raise NotImplementedError()

    def update_page(self, page):
        raise NotImplementedError()

    def remove_page(self, title):
        for report_key in self.report_keys:
            self.reports[report_key].remove(title)

    def set(self, report_key, *args):
        self.reports[report_key].set(*args)

    def remove(self, report_key, *args):
        self.reports[report_key].remove(*args)

    def create_reports(self):
        self.reports = {}
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
            if report_key in self.entries:
                report.entries = self.entries[report_key]
