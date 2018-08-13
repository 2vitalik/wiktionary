from projects.reports.lib.reports.base import BaseReportPage


class BaseListReport(BaseReportPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entries = []

    @property
    def content(self):
        return ''.join(self.entries)
