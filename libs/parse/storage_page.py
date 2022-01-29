from core.storage.main import MainStorage
from libs.parse.sections.page import Page


class IteratedStoragePage(Page):
    def __init__(self, title, content, info, silent=False):
        is_redirect = info.endswith('R')

        super().__init__(title, content, is_redirect=is_redirect,
                         silent=silent)


class StoragePage(IteratedStoragePage):  # todo: rename to `SingleStoragePage`
    storage = MainStorage()

    def __init__(self, title, silent=False, skip_absent=False):
        content = self.storage.get(title, 'content', silent=skip_absent)
        info = self.storage.get(title, 'info', silent=skip_absent)

        super().__init__(title, content, info, silent=silent)
