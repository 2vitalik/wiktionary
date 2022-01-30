import re

from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.data.blocks.detailed.translation.translations import \
    TranslationsData
from libs.parse.utils.decorators import parsing


class TranslationData(BaseBlockData):
    def remove_blank(self, value):
        value = re.sub('{{перев-блок\|?[^\n]*', '', value,  # todo: брать инфу из `translations-data` ↓
                       flags=re.UNICODE | re.DOTALL)
        value = re.sub('\|[-\w.]+=', '', value)
        value = re.sub('<!--[^-]+-->', '', value)
        value = self.remove_bottom_templates(value)
        value = value.replace(u'}}', '').replace(u'|', '').replace(u'[[]]', '')
        return value.strip()

    # todo: mark "[[]]" as an error?

    @parsing
    def _parse(self):
        self._sub_data = {
            'has_data': self.remove_blank(self.base.content) != '',  # todo: perhaps redundant?
            'translations': TranslationsData(self.base, self, self.page),
        }
