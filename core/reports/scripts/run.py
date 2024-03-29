from datetime import datetime
from os.path import join

from core.conf.conf import REPORTS_PATH
from core.storage.main import storage
from core.storage.postponed.base_updater import PostponedUpdaterMixin
from libs.sync.saver import sync_save_page
from libs.utils.dt import dt
from libs.utils.lock import locked_repeat
from libs.utils.log import log_exception
from core.reports.reports.bucket import Bucket


class ReportsUpdater(PostponedUpdaterMixin):
    path = join(REPORTS_PATH)

    def __init__(self, report_classes=None, only_recent=False):
        print(datetime.now(), 'started reports updater')
        self.only_recent = only_recent
        self.report_classes = report_classes
        self.reports = self.get_reports()

    def run(self, limit=None):
        if self.only_recent:
            self._recent()
        else:
            self._all(limit)

    def _all(self, limit=None):
        iterator = storage.iterate_pages(silent=True, limit=limit)
        for i, (title, page) in enumerate(iterator):
            self._debug_title(i, title)
            if not i % 100000:
                print(dt(), i)
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
        for report in self.reports:
            report.update_page(page)
        self._debug_processed()

    def remove_page(self, title):
        for report in self.reports:
            report.remove_page(title)

    def get_reports(self):
        if self.report_classes:
            return Bucket.create_reports(self.report_classes)
        return Bucket.get_reports(self.only_recent)

    def import_entries(self, suffix=''):
        for report in self.reports:
            report.import_entries(suffix)

    def export_entries(self, suffix=''):
        for report in self.reports:
            report.export_entries(suffix)

    def convert_entries(self):
        for report in self.reports:
            report.convert_entries()


class ReportsSaver:
    def __init__(self):
        print(datetime.now(), 'started reports saver')
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
                sub_node = value  # здесь value -- это секция (node: dict)
                new_prefix = f'{prefix}/{key}'
                self._save_reports(sub_node, key, new_prefix)  # рекурсивно
            else:
                report = value  # здесь value -- это отчёт (Report)
                report.save(self.root, self.debug)

    def _save_node(self, node: dict, key: str, prefix: str):
        title = f'{self.root}{prefix}'

        content = ''
        if key:
            content = f"Раздел: '''{key}'''\n\n"
        content += f"Подразделы:\n"
        content += self._get_node_content(node) or "* ''пусто''"

        desc = 'Обновление дерева отчётов'
        sync_save_page(title, content, desc, self.debug)

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


@log_exception('reports-all')
@locked_repeat('reports')
def reports_all(limit=None):
    ReportsUpdater().run(limit=limit)
    ReportsSaver().save()


@log_exception('reports-recent')
@locked_repeat('reports')
def reports_recent():
    ReportsUpdater(only_recent=True).run()
    ReportsSaver().save()


@log_exception('reports-some')
@locked_repeat('reports')
def reports_some(reports_classes, limit=None):
    ReportsUpdater(reports_classes).run(limit=limit)
    ReportsSaver().save()


@log_exception('reports-debug')
@locked_repeat('reports')
def reports_debug(limit=None):
    ReportsUpdater().run(limit=limit)
    ReportsSaver().save(debug=True)


@log_exception('reports-some-debug')
@locked_repeat('reports')
def reports_some_debug(reports_classes, limit=None):
    ReportsUpdater(reports_classes).run(limit=limit)
    ReportsSaver().save(debug=True)


if __name__ == '__main__':
    # reports_debug(30000)
    # reports_recent()
    # reports_all()
    # ReportsUpdater().run()
    # ReportsSaver().save()
    reports_some_debug([VerbsWithoutTranscription])
