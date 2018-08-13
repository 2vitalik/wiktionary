from projects.reports.lib.reports.dict_report.dict_of_lists.base import \
    DictOfLists


class SubLists(DictOfLists):
    sub_list_type = '*'

    def convert_sub_list_value(self, value):
        value = self.convert_value(value)
        return f'{self.list_type}{self.sub_list_type} {value}\n'

    def entry_content(self, key):
        values = ''.join(self.convert_sub_list_value(value)
                         for value in self._entries[key])
        key = self.convert_key(key)
        return f'{self.list_type} {key}\n{values}'
