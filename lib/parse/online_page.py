from lib.parse.page import BasePage
from lib.utils.wikibot import load_page


class OnlinePage(BasePage):
    def __init__(self, title):
        content = load_page(title)
        # todo: process `is_redirect`
        super().__init__(title, content)
