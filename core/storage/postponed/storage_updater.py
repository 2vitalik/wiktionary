from core.logs.mixins import StorageLogsMixin
from core.storage.main import storage
from core.storage.postponed.base_updater import PostponedUpdaterMixin


class StoragePostponedUpdaterMixin(PostponedUpdaterMixin, StorageLogsMixin):
    storage_class = None  # should be set in inheritor

    def __init__(self, process_all=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_all = process_all
        self.storage = self.storage_class(lock_slug=self.slug)

    @property
    def path(self):
        return self.storage.path

    def run(self, limit=None):  # todo: merge/integrate with `ReportsUpdater`
        if self.process_all:
            self.process_all_pages(limit)
        else:
            self.process_recent_pages()
        self.close()

    def process_all_pages(self, limit=None):  # todo: merge/integrate with `ReportsUpdater`
        iterator = storage.iterate_pages(silent=True, limit=limit)
        for i, (title, page) in enumerate(iterator):
            self._debug_title(i, title)
            if self.process_page(page) and not i % 100:
                self.save_titles()

    def process_page(self, page):
        raise NotImplementedError()

    def remove_page(self, title):
        self.storage.delete(title)

    @property
    def slug(self):
        return 'all' if self.process_all else 'recent'

    def close(self):
        self.save_titles()
        self.storage.unlock(self.slug)

    def save_titles(self):
        titles = []
        for title, info in self.storage.iterate():
            titles.append(title)
        self.storage.save_titles(titles)

        self._debug_titles_saved()
