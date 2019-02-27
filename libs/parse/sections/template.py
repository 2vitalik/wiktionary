import re

from libs.parse.patterns import find_templates
from libs.parse.utils.decorators import parsed, parsing


def tpl_pack(value):
    return value.replace('|', '\1').replace('=', '\2')


def tpl_unpack(value):
    return value.replace('\1', '|').replace('\2', '=')


class Template:
    def __init__(self, name, content=None, base=None, silent=None):
        self.name = name
        if not content:
            content = '{{' + name + '}}'
        self.content = content
        self.base = base
        self.page_title = None
        self.silent = False
        if base is not None:
            self.page_title = base.title  # todo: Проверить, что `page_title` работает правильно...
            self.silent = base.silent
        if silent is not None:
            self.silent = silent

        self.is_parsing = False
        self.parsed = False

        self._full_name = None
        self._params = None
        self._args = None
        self._kwargs = None
        self._all_args_order = None
        self._old_content = content

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

    @full_name.setter
    @parsed
    def full_name(self, value):
        # todo: full mechanism of left and right bounds
        if self._full_name.endswith('\n') and not value.endswith('\n'):
            value += '\n'
        self._full_name = value

    @property
    @parsed
    def params(self):
        return self._params

    @property
    @parsed
    def args(self):
        return self._args

    @property
    @parsed
    def kwargs(self):
        return self._kwargs

    @property
    @parsed
    def all_args_order(self):
        return self._all_args_order

    @parsed
    def find_key(self, item):
        for key in self.kwargs:
            if key.strip() == item.strip():
                return key
        return None

    @parsed
    def __getitem__(self, item):
        if type(item) == int:
            try:
                return self.args[item]
            except IndexError:
                return None
        else:
            key = self.find_key(item)
            return self.kwargs[key] if key else None

    @parsed
    def __setitem__(self, key, new_value):

        def get_bounds(value):
            if not value.strip():  # пустое значение
                if not value:
                    return '', ''
                if len(value) == 1:
                    return '', value
                else:
                    return value[0], value[1:]
            else:
                left = re.search('^\s*', value).group(0)
                right = re.search('\s*$', value).group(0)
                return left, right

        old_value = self[key]
        last_key_left, last_key_right = '', ''
        if old_value is None:
            # добавление *нового* ключа (старого значения нет)
            if self.all_args_order:
                # пробуем взять отступы значения *последнего* ключа
                last_key = self.all_args_order[-1]
                old_left, old_right = get_bounds(self[last_key])
                last_key_left, last_key_right = get_bounds(last_key)
            else:
                # шаблон пока совсем пуст, берём отступы по умолчанию
                old_left, old_right = '', ''
        else:
            # изменение текущего ключа, берём его отступы
            old_left, old_right = get_bounds(old_value)

        # отступы у нового значения
        new_left, new_right = get_bounds(new_value)

        # добавляем отступы к значению, если нужно
        if not new_left:
            new_value = f'{old_left}{new_value}'
        if not new_right:
            new_value = f'{new_value}{old_right}'

        if old_value is None:
            # добавление нового ключа:
            if type(key) == int:
                for _ in range(key - len(self.args)):
                    # добавляем промежуточные пустые значения:
                    self.append_arg(f"{old_left}{old_right}")
                self.append_arg(new_value)
            else:
                # добавляем отступы к ключу, если нужно:
                new_key_left, new_key_right = get_bounds(key)
                if not new_key_left:
                    key = f'{last_key_left}{key}'
                if not new_key_right:
                    key = f'{key}{last_key_right}'

                self.all_args_order.append(key)
                self.kwargs[key] = new_value
        else:
            # изменение существующего ключа:
            if type(key) == int:
                self.args[key] = new_value
            else:
                key = self.find_key(key)
                self.kwargs[key] = new_value

    @parsed
    def append_arg(self, value):
        self.all_args_order.append(len(self.args))
        self.args.append(value)

    @parsing
    def _parse(self):
        if self.content[:2] != '{{' or self.content[-2:] != '}}':
            raise Exception('Wrong value for Template.content.')

        self._args = []
        self._kwargs = {}
        self._all_args_order = []
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
                if key in self._kwargs and not self.silent:
                    raise TemplateKeyDuplicatedError(self, key)
                self._kwargs[key] = value
                self._all_args_order.append(key)
            else:
                self._all_args_order.append(len(self._args))
                self._args.append(restored)

    def constructed_content(self):
        content = '{{' + self.full_name
        for key in self.all_args_order:
            if type(key) == int:
                content += '|' + self.args[key]
            else:
                content += f'|{key}=' + self.kwargs[key]
        content += '}}'
        return content

    @property
    def new_content(self):
        constructed_content = self.constructed_content()
        constructed_changed = \
            constructed_content and constructed_content != self._old_content
        field_content_changed = self.content != self._old_content
        if constructed_changed and field_content_changed:
            raise Exception('Both contents types was changed, ambiguity.')
        if field_content_changed:
            content = self.content
        elif constructed_changed:
            content = constructed_content
        else:
            content = self._old_content
        return content


class TemplateKeyDuplicatedError(Exception):
    def __init__(self, template, key):
        message = f'Duplicated key "{key}" in template "{template.name}" ' \
                  f'in page "{template.page_title}"'  # todo: Проверить, что `page_title` работает
        super().__init__(message)
        self.template = template
        self.key = key
