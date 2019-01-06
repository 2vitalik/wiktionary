from pywikibot import NoPage

from core.logs.mixins import StorageLogsMixin


class BaseProcessor(StorageLogsMixin):
    def __init__(self, slug):
        self.slug = slug
        self.storage = None  # should be set in inheritor

    def process_page(self, page):
        title = page.title()  # todo: except InvalidTitle ?
        self.log_day('titles', title)
        try:
            content = page.get(get_redirect=True)
            edited = page.editTime()
            redirect = page.isRedirectPage()
        except NoPage:
            self.process_delete(title)
            self.log_day('deleted', title)
            return title, None

        self.process_update(title, content, edited, redirect)
        return title, edited

    def process_delete(self, title):
        raise NotImplementedError()

    def process_update(self, title, content, edited, redirect):
        raise NotImplementedError()

    def close(self, *args, **kwargs):
        pass

    @property
    def latest_edited(self):
        return self.storage.latest_edited

    @latest_edited.setter
    def latest_edited(self, value):
        self.storage.latest_edited = value

    @property
    def all_pages_start_from(self):
        return self.storage.all_pages_start_from

    @all_pages_start_from.setter
    def all_pages_start_from(self, value):
        self.storage.all_pages_start_from = value
