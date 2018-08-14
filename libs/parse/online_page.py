from libs.parse.sections.page import Page
from libs.utils.wikibot import load_page


class OnlinePage(Page):
    def __init__(self, title, silent=False):
        content = load_page(title)
        # todo: process `is_redirect`
        super().__init__(title, content, silent)
