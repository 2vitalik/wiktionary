from core.storage.main import MainStorage
from libs.parse.sections.page import Page


class StoragePage(Page):
    storage = MainStorage()

    def __init__(self, title, silent=False, skip_absent=False):
        content = self.storage.get(title, 'content', silent=skip_absent)
        info = self.storage.get(title, 'info', silent=skip_absent)
        is_redirect = info.endswith('R')
        super().__init__(title, content, is_redirect=is_redirect,
                         silent=silent)
