from projects.reports.lib.reports.base import BaseReportPage


class BaseDictReport(BaseReportPage):
    list_type = '#'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entries = {}

    def entry_content(self, key):
        raise NotImplementedError()

    @property
    def content(self):
        return ''.join(self.entry_content(key) for key in self._entries)
