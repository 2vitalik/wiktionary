from core.reports.lib.details_sublist.base import BaseListDetails


class SubLists(BaseListDetails):
    sub_list_type = '*'

    @classmethod
    def convert_sub_list_value(cls, value):
        value = cls.convert_value(value)
        return f'\n{cls.list_type}{cls.sub_list_type} {value}'

    @classmethod
    def convert_details(cls, details):
        values = ''.join(cls.convert_sub_list_value(value)
                         for value in details)
        return values
