from lib.parse.groupers.content.templates.base import BaseTemplatesGrouper
from lib.parse.sections.template import Template


class FilteredTemplatesGrouper(BaseTemplatesGrouper):
    def __init__(self, base_grouper, names):
        super().__init__(base_grouper)
        self.names = names

    def __iter__(self):
        for path, (tpl_name, tpl_content) in self.iter_templates():
            if not self.names or tpl_name in self.names:
                yield path, Template(tpl_name, tpl_content)
