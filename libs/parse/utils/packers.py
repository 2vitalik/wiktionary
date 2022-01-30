
from libs.parse.patterns import find_templates
from libs.utils.parse import find_comments


class TemplatesPacker:
    def __init__(self, *args, **kwargs):
        self.packed_data = {}
        super(TemplatesPacker, self).__init__(*args, **kwargs)

    def pack_templates(self, content):
        packed_content = content
        entries = find_comments(content) + \
            list(find_templates(content, only_content=True))
        for sub_content in entries:
            key = f'\1{len(self.packed_data)}\2'
            self.packed_data[key] = sub_content
            packed_content = packed_content.replace(sub_content, key)
        return packed_content

    def unpack_templates(self, packed_content):
        content = packed_content
        for key, tpl_content in reversed(list(self.packed_data.items())):
            content = content.replace(key, tpl_content)
        return content
