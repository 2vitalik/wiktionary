import re
from os.path import join, exists

from core.conf.conf import REPORTS_PATH
from libs.sync.saver import sync_save_page
from libs.utils.io import json_dump, json_load


class BaseReportPage:
    path = None
    description = None
    short_title = None

    def __init__(self,
                 path: str = None,
                 description: str = None):
        if path:
            self.path = path
        if description:
            self.description = description

    @property
    def content(self):
        raise NotImplementedError()

    @staticmethod
    def get_page_content(content, short_title=None, description=None):
        content = content or "* ''пусто''"
        short_title = short_title or 'Содержимое отчёта'

        description_block = ''
        if description:
            description = re.sub('^ +', '', description.strip(),
                                 flags=re.MULTILINE)
            description_block = \
                f'== Описание отчёта ==\n' \
                f'{description}\n' \
                f'\n'

        return f'{description_block}' \
               f"== {short_title} ==\n" \
               f"{content}".replace('\u200e', '�')

    @property
    def page_content(self):
        return self.get_page_content(self.content, self.short_title,
                                     self.description)

    def save(self,
             root_prefix: str,
             debug: bool = False):
        """
        Сохранение содержимого отчёта в ВС
        """
        title = f'{root_prefix}/{self.path}'
        content = self.page_content
        desc = f'Обновление отчёта: {self.count}'
        sync_save_page(title, content, desc, debug)


class ImportExportMixin:
    def entries_filename(self, suffix=''):
        name = self.__class__.__name__
        return join(REPORTS_PATH, f'entries{suffix}', f'{name}.json')

    def export_entries(self, suffix=''):
        json_dump(self.entries_filename(suffix), self.entries)

    def import_entries(self, suffix=''):
        filename = self.entries_filename(suffix)
        if not exists(filename):
            print(f'ImportEntriesError: File not found: "{filename}"')
            return
        self.entries = json_load(filename)


class BaseIterableReport(ImportExportMixin, BaseReportPage):
    list_type = '#'
    separator = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = {}

    def set(self, key, details):
        if details:
            self.entries[key] = details
        else:
            self.remove(key)

    def remove(self, key):
        if key in self.entries:
            del self.entries[key]

    def update_page(self, page):
        details = self.check_page(page)
        self.set(page.title, details)

    def remove_page(self, title):
        self.remove(title)

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

    def report_pages(self) -> list:
        return [self]  # return itself
