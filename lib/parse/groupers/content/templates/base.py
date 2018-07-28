from lib.parse.groupers.base import BaseGrouper
from lib.parse.patterns import find_templates


class BaseTemplatesGrouper(BaseGrouper):
    def __init__(self, base_grouper):
        super().__init__(base_grouper)
        self.fields = self.base.fields + ('tpl', )

    def iter_templates(self):
        for path, section in self.base:
            for (tpl_content, tpl_name) in find_templates(section.content):
                yield path, (tpl_name.strip(), tpl_content)
