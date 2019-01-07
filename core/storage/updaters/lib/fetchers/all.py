from datetime import datetime

from pywikibot.pagegenerators import AllpagesPageGenerator

from core.storage.updaters.lib.fetchers.base import BaseFetcher


class AllPagesFetcher(BaseFetcher):
    slug = 'all_pages'

    def __init__(self, updater_class, namespace, stopper=None,
                 start_from=None):
        """
        :param updater_class: subclass of class `BaseUpdater`
        :param namespaces: list of `pywikibot` namespaces
        :param stopper: object of class `BaseStopper`
        :param start_from: string
        """
        super().__init__(updater_class)
        self.namespace = namespace
        self.stopper = stopper
        self.run(start_from)
        self.updater.close()

    def run(self, start_from):
        start_from = start_from or self.updater.all_pages_start_from or '!'
        self.updater.log_day('cron', f'Processing `all_pages` from: '
                                     f'{start_from}')
        generator = \
            AllpagesPageGenerator(start=start_from, namespace=self.namespace)
        latest_title = None
        for count, page in enumerate(generator):
            title, edited = self.updater.process_page(page)
            if not edited:
                continue
            latest_title = latest_title or title
            self.updater.all_pages_start_from = title

            if self.stopper and self.stopper.check(count, title):
                break


class BaseStopper:
    def check(self, count, title):
        raise NotImplementedError()


class MinuteStopper(BaseStopper):
    def __init__(self, minute):
        self.minute = minute

    def check(self, count, title):
        return datetime.now().minute == self.minute


class CountStopper(BaseStopper):
    def __init__(self, count):
        self.count = count

    def check(self, count, title):
        return count == self.count
