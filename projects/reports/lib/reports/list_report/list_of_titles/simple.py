from projects.reports.lib.reports.list_report.base import BaseListReport


class TitlesList(BaseListReport):
    def add(self, title):
        self.entries.append(f'# [[{title}]]\n')
