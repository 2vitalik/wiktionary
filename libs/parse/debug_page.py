from libs.parse.sections.page import Page


class DebugPage(Page):
    def __init__(self, content, silent=False):
        super().__init__('JUST_FOR_DEBUG', content, silent=silent)
