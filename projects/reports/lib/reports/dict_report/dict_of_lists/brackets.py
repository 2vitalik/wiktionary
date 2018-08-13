from projects.reports.lib.reports.dict_report.dict_of_lists.base import \
    DictOfLists


class Brackets(DictOfLists):
    def entry_content(self, key):
        values = ", ".join(self.convert_value(value)
                           for value in self._entries[key])
        key = self.convert_key(key)
        return f'{self.list_type} {key} ({values})\n'
