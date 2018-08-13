from collections import defaultdict

from projects.reports.lib.reports.dict_report.base import BaseDictReport


class DictOfLists(BaseDictReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._entries = defaultdict(list)

    def entry_content(self, key):
        raise NotImplementedError()

    @classmethod
    def convert_key(cls, key):
        return key

    @classmethod
    def convert_value(cls, value):
        return value

    def add(self, key, value):
        self._entries[key].append(value)

    def set(self, key, values):
        self._entries[key] = values
