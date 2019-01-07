from datetime import datetime
from os.path import join

from core.conf.conf import REPORTS_PATH
from core.storage.main import storage
from core.storage.postponed.base_updater import PostponedUpdaterMixin
from libs.sync.saver import sync_save
from libs.utils.log import log_exception
from libs.utils.wikibot import save_page
from core.reports.lib.base import BaseReportPage
from core.reports.reports.bucket import Bucket


class ReportsUpdater(PostponedUpdaterMixin):
    path = join(REPORTS_PATH)

    def __init__(self, report_classes=None, only_recent=False):
        print(datetime.now(), 'started')
        self.only_recent = only_recent
        self.report_classes = report_classes

    def run(self, limit=None):
        if self.only_recent:
            self._recent()
        else:
            self._all(limit)

    def _all(self, limit=None):
        iterator = storage.iterate_pages(silent=True, limit=limit)
        for i, (title, page) in enumerate(iterator):
            self._debug_title(i, title)
            self.update_page(page)
        self.convert_entries()
        self.export_entries('.current')

    def _recent(self):
        if not self.latest_updated:
            self.only_recent = False
            self._all()
            self.latest_updated = storage.latest_recent_date()
            self.export_entries('.current')
            return

        self.import_entries('.current')
        self.process_recent_pages()
        self.convert_entries()
        self.export_entries('.current')

    def update_page(self, page):
        for report in self.get_reports():
            report.update_page(page)
        self._debug_processed()

    def remove_page(self, title):
        for report in self.get_reports():
            report.remove_page(title)

    def get_reports(self):
        if self.report_classes:
            return Bucket.create_reports(self.report_classes)
        return Bucket.get_reports(self.only_recent)

    def import_entries(self, suffix=''):
        for report in self.get_reports():
            report.import_entries(suffix)

    def export_entries(self, suffix=''):
        for report in self.get_reports():
            report.export_entries(suffix)

    def convert_entries(self):
        for report in self.get_reports():
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
        self._import_entries('.current')
        self._build_tree()
        self._save_reports(self.tree)

    @classmethod
    def _import_entries(cls, suffix=''):
        for report in Bucket.get_reports():
            report.import_entries(suffix)

    def _build_tree(self):
        for report in Bucket.get_reports():
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
    ReportsUpdater().run(limit=limit)
    ReportsSaver().save()


@log_exception('reports')
def reports_recent():
    ReportsUpdater(only_recent=True).run()
    ReportsSaver().save()


@log_exception('reports')
def reports_debug(limit=None):
    ReportsUpdater().run(limit=limit)
    ReportsSaver().save(debug=True)


if __name__ == '__main__':
    reports_debug(30000)
    # reports_recent()
