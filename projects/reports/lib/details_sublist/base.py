from collections import defaultdict

from projects.reports.lib.base import BaseIterableReport


class BaseListDetails(BaseIterableReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entries = defaultdict(list)

    @classmethod
    def convert_value(cls, value):
        return value

    def append(self, key, value):
        self._entries[key].append(value)

    def import_entries(self):
        self._entries = defaultdict(list)
        data = super().import_entries()
        self._entries.update(data)
