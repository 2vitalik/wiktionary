from libs.parse.data.base import BaseData


class BaseDetailedData(BaseData):
    # todo: __init__(от одного параметра, а из него уже всё остальное достать)

    @property
    def lang(self):
        return self.base_data.lang

    @property
    def parsed_data(self):
        return self.sub_data
