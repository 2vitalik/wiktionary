from core.reports.lib.details_sublist.sub_lists import SubLists
from core.reports.lib.mixins.key_title import KeyTitle
from libs.parse.sections.template import TemplateKeyDuplicatedError
from libs.utils.wikicode import code


class ValueCustom:
    @classmethod
    def convert_value(cls, value):
        template, key = value  # unpack
        return code(key) + ' в {{template|' + template + '}}'


class TemplateKeyDuplicated(KeyTitle, ValueCustom, SubLists):
    path = 'Ошибки/Важные/Шаблоны/Разное/Дублирование параметров'
    short_title = 'Дублирование параметров в шаблонах'

    def check_page(self, page) -> list:
        values = []
        for template in page.templates.last_list():
            template.silent = False
            try:
                _ = template.params
            except TemplateKeyDuplicatedError as e:
                values.append((e.template.name, e.key))
        return values
