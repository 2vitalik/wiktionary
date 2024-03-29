import re

from libs.parse.groupers.content.templates.base import BaseTemplatesGrouper
from libs.parse.sections.template import Template


class FilteredTemplatesGrouper(BaseTemplatesGrouper):
    def __init__(self, base_grouper, names, **kwargs):
        super().__init__(base_grouper)
        self.names = names
        self.patterns = kwargs.get('re')

    def __iter__(self):
        for _, template in self.iterate():
            yield _, template  # todo: fix to return only `template`?

    def iterate(self):
        for path, (tpl_name, tpl_content) in self.iter_templates():
            iter_all = not self.names and not self.patterns
            iter_names = False
            if self.names:
                for name in self.names:
                    if type(name) == list:
                        if tpl_name in name:
                            iter_names = True
                            break
                    elif type(name) == str:
                        if tpl_name == name:
                            iter_names = True
                            break
                    else:
                        raise Exception('Unknown argument for filtering '
                                        'templates')
            iter_re = False
            if self.patterns:
                if type(self.patterns) == str:
                    self.patterns = [self.patterns]
                for pattern in self.patterns:
                    if re.match(pattern, tpl_name):
                        iter_re = True
            if iter_all or iter_names or iter_re:
                yield path, Template(tpl_name, tpl_content, base=self.base)
