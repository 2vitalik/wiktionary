from projects.reports.lib.details_sublist.base import \
    BaseListDetails


class Colon(BaseListDetails):
    separator = ': '

    @classmethod
    def convert_details(cls, details):
        values = ", ".join(cls.convert_value(value)
                           for value in details)
        return values
