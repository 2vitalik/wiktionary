from libs.parse.utils.decorators import parsed, parsing


class BaseData:
    def __init__(self, base):
        self.base = base
        self._sub_data = None

        self.is_parsing = False
        self.parsed = False

    @property
    @parsed
    def sub_data(self):
        return self._sub_data

    @parsed
    def __getitem__(self, index):
        # Непосредственное обращение к дочернему элементу?
        if index in self.sub_data:
            return self.sub_data[index]

        # Обращение по числовому индексу?
        if type(index) == int:
            key = list(self.sub_data.keys())[int(index)]
            return self.sub_data[key]

        ...  # todo

    @parsed
    def __getattr__(self, attr):
        if attr in self.sub_data:
            return self.sub_data[attr]

        return None  # todo?

    @parsing
    def _parse(self):
        pass
