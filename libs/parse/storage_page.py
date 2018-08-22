from core.storage.main import MainStorage
from libs.parse.sections.page import Page


class StoragePage(Page):
    storage = MainStorage()

    def __init__(self, title, silent=False):
        content = self.storage.get(title, 'content')
        # todo: process `is_redirect`
        super().__init__(title, content, silent=silent)
