import re

from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.utils.packers import TemplatesPacker
from libs.utils.parse import remove_comments


class BaseSemanticData(TemplatesPacker, BaseBlockData):
    def check_empty(self, value):
        value = re.sub('{{\s*пример[|\s]*(перевод=)?[|\s]*\}\}', '', value)  # obsolete, because of next one?
        value = re.sub('{{\s*пример[|\s]*(\|[^|=}]+=)+[|\s]*\}\}', '', value)
        value = re.sub('{{\s*Нужен перевод\s*(\|[-\w]+)?[|\s]*\}\}', '', value)
        value = re.sub('{{\s*(Нужен дополнительный перевод|Нужен однословный перевод|значение\?|\?\?)\s*\}\}', '', value)
        value = re.sub('{{\s*\?[^}]*\}\}', '', value)  # {{?}}
        value = re.sub('{{\s*помета\.[^}]*\}\}', '', value)
        value = re.sub('{{\s*помета\|?\??\s*\}\}', '', value)
        value = re.sub('{{\s*илл\|[^}]+\}\}', '', value)
        value = re.sub('{{\s*списки семантических связей[^}]*\}\}', '', value)
        value = re.sub('<!--(.*?)-->', '', value, flags=re.DOTALL)
        return value.strip() in ['', '#']

    def get_entries(self):
        packed_content = \
            self.pack_templates(remove_comments(self.base.content))
        for line in packed_content.split('\n'):
            yield self.unpack_templates(line)
