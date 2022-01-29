from pywikibot import NoPage
from shared_utils.api.slack.core import post_to_slack

from core.logs.mixins import StorageLogsMixin
from libs.utils.debug import debug
from libs.utils.dt import dt


class BaseUpdater(StorageLogsMixin):
    def __init__(self, slug):
        self.slug = slug
        self.storage = None  # should be set in inheritor

    def process_page(self, page):
        title = page.title()  # todo: except InvalidTitle ?
        self._debug_title(title)
        self.log_day('titles', title)
        # if self.slug == 'recent':
        #     post_to_slack(f'{self.slug}-titles',
        #                   f'<https://ru.wiktionary.org/wiki/{title}|{title}>')
        try:
            content = page.get(get_redirect=True)
            edited = page.editTime()
            redirect = page.isRedirectPage()
        except NoPage:
            self.remove_page(title)
            self.log_day('deleted', title)
            post_to_slack(f'{self.slug}-deleted',
                          f'<https://ru.wiktionary.org/wiki/{title}|{title}>')
            return title, None

        self.update_page(title, content, edited, redirect)
        return title, edited

    def update_page(self, title, content, edited, redirect):
        raise NotImplementedError()

    def remove_page(self, title):
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

    @debug
    def _debug_title(self, title):
        print(dt(), title)
