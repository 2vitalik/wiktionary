import re

from libs.parse.patterns import find_templates
from libs.parse.utils.decorators import parsed, parsing


def tpl_pack(value):
    return value.replace('|', '\1').replace('=', '\2')


def tpl_unpack(value):
    return value.replace('\1', '|').replace('\2', '=')


class Template:
    def __init__(self, name, content, base=None):
        self.name = name
        self.content = content
        self.base = base
        if base:
            self.title = base.title

        self.is_parsing = False
        self.parsed = False

        self._full_name = None
        self._args = None
        self._kwargs = None
        self._params = None

    def __str__(self):
        class_name = type(self).__name__
        return f'{class_name}({self.name})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name and self.content == other.content

    @property
    @parsed
    def full_name(self):
        return self._full_name

    @property
    @parsed
    def args(self):
        return self._args

    @property
    @parsed
    def params(self):
        return self._params

    @property
    @parsed
    def kwargs(self):
        return self._kwargs

    @parsing
    def _parse(self):
        if self.content[:2] != '{{' or self.content[-2:] != '}}':
            raise Exception('Wrong value for Template.content.')

        self._args = []
        self._kwargs = {}
        content = self.content[2:-2]

        for link_content in re.findall('\[\[[^]]+\]\]', content):
            content = content.replace(link_content, tpl_pack(link_content))
        for tpl_content, tpl_name in find_templates(content):
            content = content.replace(tpl_content, tpl_pack(tpl_content))

        parts = content.split('|')
        self._full_name = parts[0]
        self._params = tpl_unpack('|'.join(parts[1:]))
        for part in parts[1:]:
            restored = tpl_unpack(part)
            if '=' in part:
                key, value = restored.split('=', maxsplit=1)
                if key in self._kwargs:
                    msg = f'Duplicated key "{key}" in template "{self.name}"' \
                          f'in page "{self.base.title}".'
                    raise Exception()
                self._kwargs[key] = value
            else:
                self._args.append(restored)
