from datetime import datetime
from os.path import join

from core.conf.conf import REPORTS_PATH
from core.storage.main import storage
from core.storage.postponed.mixins import PostponedUpdaterMixin
from libs.sync.saver import sync_save
from libs.utils.log import log_exception
from libs.utils.wikibot import save_page
from core.reports.lib.base import BaseReportPage
from core.reports.reports.bucket import Bucket


class ReportsUpdater(PostponedUpdaterMixin):
    path = join(REPORTS_PATH)

    def __init__(self):
        print(datetime.now())
        super().__init__()

    def all(self, limit=None):
        for title, page in storage.iterate_pages(silent=True, limit=limit):
            self.process_page(page, via_recent=False)
        self.convert_entries()
        self.export_entries('.all')

    def recent(self):
        if not self.latest_updated:
            self.all()
            self.latest_updated = storage.latest_recent_date()
            self.export_entries('.recent')
            return

        self.import_entries('.recent')
        self.process_recent_pages()
        self.convert_entries()
        self.export_entries('.recent')

    def process_page(self, page, via_recent):
        for report in Bucket.reports.values():
            report.process_page(page, via_recent)

    def remove_page(self, title, via_recent):
        for report in Bucket.reports.values():
            report.remove_page(title, via_recent)

    @classmethod
    def import_entries(cls, suffix=''):
        for report in Bucket.reports.values():
            report.import_entries(suffix)

    @classmethod
    def export_entries(cls, suffix=''):
        for report in Bucket.reports.values():
            report.export_entries(suffix)

    @classmethod
    def convert_entries(cls):
        for report in Bucket.reports.values():
            report.convert_entries()


class ReportsSaver:
    def __init__(self):
        self.debug = False
        self.root = 'Викисловарь:Отчёты/v3'
        # self.root = 'Участник:Vitalik/Отчёты/v3'
        self.tree = {
            'Ошибки': {
                'Важные': {},
                'Средние': {},
                'Лёгкие': {},
            },
            'Отчёты': {},
        }

    def save(self, debug=False, root=None):
        if debug:
            self.debug = debug
        if root:
            self.root = root
        self._build_tree()
        self._save_reports(self.tree)

    def _build_tree(self):
        for report in Bucket.reports.values():
            for report_page in report.report_pages():
                keys = report_page.path.split('/')
                curr = self.tree
                for key in keys[:-1]:
                    if key not in curr:
                        curr[key] = {}
                    curr = curr[key]
                key = keys[-1]
                if key in curr:
                    raise Exception(f'Duplicated report: {report_page.path}')
                curr[key] = report_page

    def _save_reports(self, node: dict, key='', prefix=''):
        self._save_node(node, key, prefix)
        for key, value in node.items():
            if type(value) == dict:
                # value -- это секция
                new_prefix = f'{prefix}/{key}'
                self._save_reports(value, key, new_prefix)  # рекурсивно
            else:
                # value -- это отчёт
                self._save_report(value)

    def _save_node(self, node: dict, key: str, prefix: str):
        title = f'{self.root}{prefix}'

        content = ''
        if key:
            content = f"Раздел: '''{key}'''\n\n"
        content += f"Подразделы:\n"
        content += self._get_node_content(node) or "* ''пусто''"

        desc = 'Обновление дерева отчётов'
        self._save_page(title, content, desc)

    def _get_node_content(self, node: dict, indent=1, prefix='/'):
        content = ''
        asterisks = '*' * indent
        for key, value in node.items():
            link = f'[[{prefix}{key}|{key}]]'
            if type(value) == dict:
                # value -- это секция
                content += f"{asterisks} {link}\n"
                new_prefix = f'{prefix}{key}/'
                content += self._get_node_content(value, indent + 1, new_prefix)
            else:
                # value -- это отчёт
                report = value
                if report.count:
                    styled_count = f"'''{report.count}'''"
                else:
                    styled_count = f"<span style='color: silver'>0</span>"
                content += f"{asterisks} '''{link}''' ({styled_count})\n"
        return content

    def _save_report(self, report: BaseReportPage):
        title = f'{self.root}/{report.path}'
        content = report.page_content
        desc = f'Обновление отчёта: {report.count}'
        self._save_page(title, content, desc)

    def _save_page(self, title, content, desc):
        sync_save(title, content)
        if self.debug:
            print(f'{"=" * 100}\n{title}\n{content.strip()}\n')
        else:
            save_page(title, content, desc)


@log_exception('reports')
def reports_all(limit=None):
    ReportsUpdater().all(limit=limit)
    ReportsSaver().save()


@log_exception('reports')
def reports_recent():
    ReportsUpdater().recent()
    ReportsSaver().save(root='Участник:Vitalik/Отчёты/v3')


@log_exception('reports')
def reports_debug(limit=None):
    ReportsUpdater().all(limit=limit)
    ReportsSaver().save(debug=True)


if __name__ == '__main__':
    reports_debug(30000)
    # reports_recent()