from lib.parse.groupers.base import BaseGrouper
from lib.parse.groupers.content.templates.all import TemplatesGrouper


class BaseSectionsGrouper(BaseGrouper):
    @property
    def templates(self):
        return TemplatesGrouper(self)
