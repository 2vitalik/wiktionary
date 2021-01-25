from libs.parse.sections.page import Page


class DebugPage(Page):
    def __init__(self, content, site_lang: str, silent=False):
        super().__init__('JUST_FOR_DEBUG', content, site_lang, silent=silent)
