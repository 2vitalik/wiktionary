from pprint import pprint

from core.storage.main import MainStorage
from libs.utils.wikibot import save_page
from projects.reports.lib.report_page import ReportPage
from projects.reports.reports.bucket import Bucket


class RunAllReports:
    root = 'Участник:Vitalik/Отчёты/v3'
    tree = {
        'Ошибки': {
            'Важные': {},
            'Средние': {},
            'Лёгкие': {},
        },
        'Отчёты': {},
    }

    def __init__(self):
        self.storage = MainStorage()
        self._check_pages()
        self._build_tree()
        self._save_reports(self.tree)

    def _check_pages(self):
        for title, page in self.storage.iterate_pages(silent=True):
            for report in Bucket.reports.values():
                report.check(page)

    def _build_tree(self):
        for report in Bucket.reports.values():
            for report_page in report.build():
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
        pprint(self.tree)

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
        content = ''
        if key:
            content = f"Раздел: '''{key}'''\n\n"
        content += f"Подразделы:\n"
        content += self._get_node_content(node)
        # print('=' * 100)
        # print(f'{self.root}{prefix}')
        # print(content)
        save_page(f'{self.root}{prefix}', content, '/Тестовое/ Обновление дерева отчётов')

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

    def _save_report(self, report: ReportPage):
        # print('=' * 100)
        # print(f'{self.root}/{report.path}')
        # print(report.content)
        save_page(f'{self.root}/{report.path}', report.content,
                  f'/Тестовое/ Обновление отчёта: {report.count}')


if __name__ == '__main__':
    RunAllReports()
