from pywikibot import NoPage

from core.storage.main import MainStorage
from lib.utils.dt import dt
from lib.utils.log import log_day, log_hour


class BaseStorageUpdater:
    def __init__(self):
        self.storage = MainStorage(lock=True)

    def process_page(self, page):
        title = page.title()  # todo: except InvalidTitle ?
        self.log_day('titles', title)

        try:
            content = page.get(get_redirect=True)
            edited = page.editTime()
            redirect = page.isRedirectPage()
        except NoPage:
            self.storage.delete(title)
            log_day('deleted.txt', title, path=self.storage.logs_path)
            return None

        info = f"{dt(edited, utc=True)}, {'R' if redirect else 'A'}"
        self.storage.update(title, content=content, info=info)
        self.log_hour('changed', f'<{info}> - {title}')
        return edited

    def log_day(self, slug, value):
        log_day(slug, value, path=self.storage.logs_path)

    def log_hour(self, slug, value):
        log_hour(slug, value, path=self.storage.logs_path)
