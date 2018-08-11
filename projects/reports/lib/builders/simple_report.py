import re

from projects.reports.lib.builders.base_report import BaseReportBuilder
from projects.reports.lib.report_page import ReportPage


class SimpleReportBuilder(BaseReportBuilder):
    path = None
    desc = None

    entries = []

    def check(self, page):
        if self.check_bool(page):
            self.entries.append(f'# [[{page.title}]]\n')

    def check_bool(self, page) -> bool:
        raise NotImplementedError()

    def build(self) -> list:
        if not self.path or not self.desc:
            class_name = self.__class__.__name__
            raise Exception(f'{class_name}: Absent values `path` or `desc`')

        desc = re.sub('^ +', '', self.desc.strip(), flags=re.MULTILINE)
        content = f'== Описание отчёта ==\n{desc}\n\n' \
                  f"== Список статей ==\n{''.join(self.entries)}"
        return [ReportPage(self.path, len(self.entries), content)]
