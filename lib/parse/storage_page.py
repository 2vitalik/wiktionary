from core.storage.main import MainStorage
from lib.parse.page import BasePage


class StoragePage(BasePage):
    storage = MainStorage()

    def __init__(self, title):
        content = self.storage.get(title, 'content')
        # todo: process `is_redirect`
        super().__init__(title, content)


if __name__ == '__main__':
    p = StoragePage('сало')
    print(p.langs['ru'].homonyms[''].sections['Семантические свойства'].
          sub_sections['Значение'].content)
