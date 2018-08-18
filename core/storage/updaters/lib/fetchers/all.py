from datetime import datetime

from pywikibot.pagegenerators import AllpagesPageGenerator

from core.storage.updaters.lib.fetchers.base import BaseFetcher


class AllPagesFetcher(BaseFetcher):
    slug = 'all_pages'

    def __init__(self, processor_class, namespace, stopper=None,
                 start_from=None):
        super().__init__(processor_class)
        self.namespace = namespace
        self.stopper = stopper
        self.run(start_from)
        self.processor.close()

    def run(self, start_from):
        start_from = start_from or self.processor.all_pages_start_from or '!'
        self.processor.log_day('cron', f'Processing `all_pages` from: '
                                       f'{start_from}')
        generator = \
            AllpagesPageGenerator(start=start_from, namespace=self.namespace)
        latest_title = None
        for count, page in enumerate(generator):
            title, edited = self.processor.process_page(page)
            print(title)
            if not edited:
                continue
            latest_title = latest_title or title
            self.processor.all_pages_start_from = title

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
