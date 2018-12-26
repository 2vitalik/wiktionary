from core.conf import conf
from core.storage.postponed.mixins import PostponedUpdaterMixin
from libs.storage.storage import Storage


class AuthorsStorage(PostponedUpdaterMixin, Storage):
    def __init__(self, lock_slug='', **kwargs):
        kwargs['path'] = conf.AUTHORS_STORAGE_PATH
        kwargs['tables'] = {
            'created': 'simple',
        }
        kwargs['lock_slug'] = lock_slug
        super().__init__(**kwargs)

    def get(self, title, silent=False, **kwargs):
        """
        Так как у нас только одна "таблица", то нет смысла принимать
        дополнительный параметр `table` (он всегда должен быть 'created')
        """
        return super().get(title, 'created', silent)

    def iterate(self, *args, **kwargs):
        """
        Так как у нас только одна "таблица", то нет смысла принимать
        дополнительный параметр `table` (он всегда должен быть 'created')
        """
        yield from super().iterate('created')

    # def iterate_pages(self, limit=None, silent=False):
    #     # todo: cyrilic= latin=...
    #     count = 0
    #     for title, content in self.iterate('content'):
    #         yield title, Page(title, content, silent=silent)
    #         count += 1
    #         if limit and count >= limit:
    #             break


authors_storage = AuthorsStorage()
