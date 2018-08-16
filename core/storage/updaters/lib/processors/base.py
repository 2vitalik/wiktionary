from pywikibot import NoPage

from libs.utils.classes import required
from libs.utils.log import log_day, log_hour


class BaseProcessor:
    def __init__(self):
        self.slug = None  # should be set later

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
            return None

        self.process_update(title, content, edited, redirect)
        return edited

    def process_delete(self, title):
        raise NotImplementedError()

    def process_update(self, title, content, edited, redirect):
        raise NotImplementedError()

    @property
    def latest_edited(self):
        raise NotImplementedError()

    def close(self, *args, **kwargs):
        pass

    @property
    def logs_path(self):
        raise NotImplementedError()

    @required('slug')
    def log_day(self, sub_slug, value):
        log_day(f"{self.slug}/{sub_slug}", value, path=self.logs_path)

    @required('slug')
    def log_hour(self, sub_slug, value):
        log_hour(f"{self.slug}/{sub_slug}", value, path=self.logs_path)
