from lib.parse.groupers.content.templates.base import BaseTemplatesGrouper
from lib.parse.groupers.content.templates.filtered import \
    FilteredTemplatesGrouper
from lib.parse.sections.template import Template


class TemplatesGrouper(BaseTemplatesGrouper):
    def __iter__(self):
        for path, (tpl_name, tpl_content) in self.iter_templates():
            yield path, Template(tpl_name, tpl_content)

    def __call__(self, *args, **kwargs):
        return FilteredTemplatesGrouper(self.base, args)

    def __getattr__(self, item):
        return FilteredTemplatesGrouper(self.base, [item])


# todo: hierarchical templates (вложенные друг в друга)
# todo: возможность возвращать пустые списки или None, если в секции нет tpl'ов
