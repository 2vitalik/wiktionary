from collections import defaultdict

from core.reports.lib.base import BaseIterableReport
from libs.sync.saver import sync_save_page
from libs.utils.numbers import get_plural
from libs.utils.unicode import unicode_sorted


class BaseLargeReport(BaseIterableReport):
    plurals = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = {}
        self._large_content = ''

    def get_short_title(self, letter):
        return self.short_title  # default value

    def get_description(self, letter):
        return self.description  # default value

    def group_entries(self):
        raise NotImplementedError()

    def save(self, root_prefix, debug=False):
        grouped = self.group_entries()
        for key, entries in grouped.items():
            content = ''.join(self.entry_content(entry) for entry in entries)
            # todo: index links to other letters?
            page_content = \
                self.get_page_content(content, self.get_short_title(key),
                                      self.get_description(key))
            count = len(entries)
            title = f'{root_prefix}/{self.path}/{key}'
            desc = f'Обновление отчёта: {count}'
            sync_save_page(title, page_content, desc)

            plural = get_plural(count, *self.plurals) if self.plurals else ''
            self._large_content += \
                f"* '''[[/{key}|{key}]]''' — '''{count}''' {plural}\n"

        super().save(root_prefix, debug)  # сохранение страницы индекса

    @property
    def content(self):
        return self._large_content
