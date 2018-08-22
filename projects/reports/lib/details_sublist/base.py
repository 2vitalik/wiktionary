from collections import defaultdict

from projects.reports.lib.base import BaseIterableReport


class BaseListDetails(BaseIterableReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = defaultdict(list)

    @classmethod
    def convert_value(cls, value):
        return value

    def append(self, key, value):
        self.entries[key].append(value)

    def import_entries(self, suffix=''):
        super().import_entries(suffix)
        new_entries = defaultdict(list)
        new_entries.update(self.entries)
        self.entries = new_entries
