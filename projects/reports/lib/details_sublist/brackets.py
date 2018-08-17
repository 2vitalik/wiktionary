from projects.reports.lib.details_sublist.base import \
    BaseListDetails


class Brackets(BaseListDetails):
    separator = ' '

    @classmethod
    def convert_details(cls, details):
        values = ", ".join(cls.convert_value(value)
                           for value in details)
        return f'({values})'
