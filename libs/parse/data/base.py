from libs.parse.utils.decorators import parsed, parsing


def parsed_data(func):
    def process(data):
        if type(data) == dict:
            return {
                key: process(value)
                for key, value in data.items()
            }
        if isinstance(data, BaseData):
            return process(data.parsed_data)
        return data  # just some value, not a dict

    def wrapped(self, *args, **kwargs):
        data = func(self, *args, **kwargs)
        return process(data)

    return wrapped


class BaseData:
    def __init__(self, section, base_data, page):
        self.base = section  # todo: rename to `section`
        self.base_data = base_data  # up to one level
        self.page = page
        self._sub_data = None

        self.is_parsing = False
        self.parsed = False

    @property
    def title(self):
        return self.page.title

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
        self._sub_data = {'error': 'NotImplementedError'}
