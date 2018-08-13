from projects.reports.lib.reports.list_report.base import BaseListReport


class DetailedTitles(BaseListReport):
    def add(self, title, details):
        self.entries.append(f'# [[{title}]]{details}\n')
