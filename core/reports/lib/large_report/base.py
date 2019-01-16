from collections import defaultdict

from core.reports.lib.base import BaseIterableReport
from libs.sync.saver import sync_save_page
from libs.utils.numbers import get_plural
from libs.utils.unicode import unicode_sorted


class BaseLargeReportMixin(BaseIterableReport):
    plurals = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = {}
        self._large_content = ''

    def get_short_title(self, letter):
        return self.short_title  # default value

    def get_description(self, letter):
        return self.description  # default value

    def save(self, root_prefix, debug=False):
        grouped = defaultdict(list)
        for key in self.entries:
            letter = key[0].upper()
            grouped[letter].append(key)

        # todo: use ALL LETTERS optionally?
        for letter in unicode_sorted(grouped.keys()):
            keys = grouped[letter]
            content = ''.join(self.entry_content(key) for key in keys)
            # todo: index links to other letters?
            page_content = \
                self.get_page_content(content, self.get_short_title(letter),
                                      self.get_description(letter))
            count = len(keys)
            title = f'{root_prefix}/{self.path}/{letter}'
            desc = f'Обновление отчёта: {count}'
            sync_save_page(title, page_content, desc)

            plural = get_plural(count, *self.plurals) if self.plurals else ''
            self._large_content += \
                f"* '''[[/{letter}|{letter}]]''' — '''{count}''' {plural}\n"

        super().save(root_prefix, debug)  # сохранение страницы индекса

    @property
    def content(self):
        return self._large_content


class PluralArticles:
    plurals = ('статья', 'статьи', 'статей')


class PluralVerbs:
    plurals = ('глагол', 'глагола', 'глаголов')
