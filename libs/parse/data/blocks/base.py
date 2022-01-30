import re

from libs.parse.data.base import BaseData, parsed_data


class BaseBlockData(BaseData):
    def remove_bottom_templates(self, content):
        content = re.sub(u'<!--[^-]+-->', '', content)
        content = re.sub(
            '{{(improve|nocat|unfinished|длина слова|Категория|DEFAULTSORT|stub)[^}]*\}\}',  # todo: use new templates mechanism?
            '',
            content, flags=re.UNICODE | re.DOTALL)
        content = re.sub('\[\[[-\w]+:[^]]+\]\]', '', content)
        content = re.sub('\[\[Категория:[^]]*\]\]', '', content,
                         flags=re.UNICODE)
        return content

    @property
    def lang(self):
        return self.base_data.lang

    def base_parsed_data(self):
        return {
            'header': True,
            'has_content': self.base.content.strip() != '',
        }

    @property
    @parsed_data
    def parsed_data(self):
        return {
            **self.base_parsed_data(),
            **self.sub_data,
        }
