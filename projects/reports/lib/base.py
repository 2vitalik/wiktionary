import re
from os.path import join

from core.conf.conf import REPORTS_PATH
from libs.utils.io import json_dump, json_load


class BaseReportPage:
    path = None
    description = None

    def __init__(self, path: str = None, description: str = None):
        if path:
            self.path = path
        if description:
            self.description = description

    @property
    def content(self):
        raise NotImplementedError()

    @property
    def page_content(self):
        description = re.sub('^ +', '', self.description.strip(),
                             flags=re.MULTILINE)
        content = self.content or "* ''пусто''"

        return f'== Описание отчёта ==\n' \
               f'{description}\n' \
               f'\n' \
               f"== Содержимое отчёта ==\n" \
               f"{content}".replace('\u200e', '�')


class BaseIterableReport(BaseReportPage):
    list_type = '#'
    separator = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = {}

    def set(self, key, details):
        if details:
            self.entries[key] = details
        else:
            if key in self.entries:
                self.remove(key)

    def remove(self, key):
        del self.entries[key]

    def process_page(self, page):
        details = self.check_page(page)
        self.set(page.title, details)

    @classmethod
    def check_page(cls, page):
        return ...  # should be implemented in inheritors

    @property
    def count(self):
        return len(self.entries)

    @property
    def content(self):
        return ''.join(self.entry_content(key) for key in self.entries)

    def entry_content(self, key):
        details = self.convert_details(self.entries[key])
        key = self.convert_key(key)
        return f'{self.list_type} {key}{self.separator}{details}\n'

    @classmethod
    def convert_key(cls, key):
        return key

    @classmethod
    def convert_details(cls, details):
        return details

    def convert_entries(self):
        pass  # can be implemented in inheritor

    @property
    def entries_filename(self):
        name = self.__class__.__name__
        return join(REPORTS_PATH, 'entries', f'{name}.json')

    def export_entries(self):
        json_dump(self.entries_filename, self.entries)

    def import_entries(self):
        self.entries = json_load(self.entries_filename)

    def report_pages(self) -> list:
        return [self]  # return itself
