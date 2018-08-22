from datetime import datetime
from os.path import join

from core.conf.conf import REPORTS_PATH
from core.storage.main import storage
from core.storage.updaters.mixins import PostponedValuesMixin
from libs.sync.saver import sync_save
from libs.utils.log import log_exception
from libs.utils.wikibot import save_page
from projects.reports.lib.base import BaseReportPage
from projects.reports.reports.bucket import Bucket


class RunAllReports(PostponedValuesMixin):
    path = join(REPORTS_PATH)

    # root = 'Участник:Vitalik/Отчёты/v3'
    root = 'Викисловарь:Отчёты/v3'
    tree = {
        'Ошибки': {
            'Важные': {},
            'Средние': {},
            'Лёгкие': {},
        },
        'Отчёты': {},
    }

    def __init__(self, debug=False, root=None):
        print(datetime.now())
        self.debug = debug
        if root:
            self.root = root

    def import_entries(self, suffix=''):
        for report in Bucket.reports.values():
            report.import_entries(suffix)
        return self

    def check_all(self, limit=None):
        pages_iterator = storage.iterate_pages(silent=True, limit=limit)
        self._check_pages(pages_iterator, recent=False)
        return self

    def check_recent(self):
        if not self.latest_updated:
            self.check_all()
            self.latest_updated = storage.latest_recent_date()
            return self

        pages_iterator = storage.iterate_recent_pages(self.latest_updated,
                                                      silent=True)
        self._check_pages(pages_iterator, recent=True)
        self.latest_updated = self.new_latest_updated
        return self

    def export_entries(self, suffix=''):
        for report in Bucket.reports.values():
            report.export_entries(suffix)
        return self

    def save(self):
        self._build_tree()
        self._save_reports(self.tree)

    def _check_pages(self, pages_iterator, recent=True):
        for row in pages_iterator:
            if recent:
                log_dt, title, page = row
                self.new_latest_updated = log_dt
            else:
                title, page = row
            for report in Bucket.reports.values():
                report.process_page(page)
        for report in Bucket.reports.values():
            report.convert_entries()

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
def reports_all(limit=None):  # todo: backup them hourly?
    runner = RunAllReports(debug=False)
    runner.check_all(limit=limit)
    runner.export_entries('.all')
    runner.save()


@log_exception('reports')
def reports_recent(initiate=False):  # todo: backup them hourly?
    runner = RunAllReports(debug=False, root='Участник:Vitalik/Отчёты/v3')
    if not initiate:
        runner.import_entries('.recent')
    runner.check_recent()
    runner.export_entries('.recent')
    runner.save()


@log_exception('reports')
def reports_debug(limit=None):
    runner = RunAllReports(debug=True)
    runner.check_all(limit=limit)
    runner.export_entries('.debug2')
    runner.save()


if __name__ == '__main__':
    reports_debug(30000)
    # reports_recent()
