from libs.parse.groupers.base import BaseGrouper
from libs.parse.groupers.content.templates.all import TemplatesGrouper


class BaseSectionsGrouper(BaseGrouper):
    @property
    def templates(self):
        return TemplatesGrouper(self)
