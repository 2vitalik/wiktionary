from core.conf import conf
from core.storage.postponed.mixins import PostponedUpdaterMixin
from libs.storage.storage import Storage


class HtmlStorage(PostponedUpdaterMixin, Storage):
    def __init__(self, lock_slug='', **kwargs):
        kwargs['path'] = conf.HTMLS_STORAGE_PATH
        kwargs['tables'] = {
            'html': 'content',
        }
        kwargs['lock_slug'] = lock_slug
        super().__init__(**kwargs)

    def get(self, title, silent=False, **kwargs):
        """
        Так как у нас только одна "таблица", то нет смысла принимать
        дополнительный параметр `table` (он всегда должен быть 'html')
        """
        return super().get(title, 'html', silent)

    def iterate(self, *args, **kwargs):
        """
        Так как у нас только одна "таблица", то нет смысла принимать
        дополнительный параметр `table` (он всегда должен быть 'html')
        """
        yield from super().iterate('html')

    # def iterate_pages(self, limit=None, silent=False):
    #     # todo: cyrilic= latin=...
    #     count = 0
    #     for title, content in self.iterate('content'):
    #         yield title, Page(title, content, silent=silent)
    #         count += 1
    #         if limit and count >= limit:
    #             break


htmls_storage = HtmlStorage()
