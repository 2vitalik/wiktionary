import re


class BaseReportPage:
    path = None
    description = None

    def __init__(self, path: str = None, description: str = None):
        if path:
            self.path = path
        if description:
            self.description = description

    _entries = None  # should be overridden in inheritors

    @property
    def entries(self):
        return self._entries

    @property
    def count(self):
        return len(self.entries)

    @property
    def content(self):
        raise NotImplementedError()

    @property
    def page_content(self):
        description = re.sub('^ +', '', self.description.strip(),
                             flags=re.MULTILINE)
        content = self.content or "* ''пусто''"

        return f'== Описание отчёта ==\n' \
               f'{description}\n' \
               f'\n' \
               f"== Содержимое отчёта ==\n" \
               f"{content}".replace('\u200e', '�')
