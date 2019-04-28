from core.conf import conf
from libs.storage.storage import Storage


class AuthorsStorage(Storage):
    def __init__(self, lock_slug='', path=None):
        super().__init__(
            path=path or conf.AUTHORS_STORAGE_PATH,
            tables={
                'created': 'simple',
            },
            max_counts={  # todo: implement such feature
                'created': ...,
            },
            lock_slug=lock_slug,
        )

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


authors_storage = AuthorsStorage()
