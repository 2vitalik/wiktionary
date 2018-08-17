
class BaseComplexReport:
    base_path = None
    base_class = None

    reports = {}
    report_keys = None

    def __init__(self):
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
            self.reports[report_key] = self.base_class(path, description)

    def report_pages(self) -> list:
        return list(self.reports.values())

    @property
    def entries(self):
        return ...  # todo

    def import_entries(self):
        pass  # todo
