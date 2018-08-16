from pywikibot import Timestamp
from pywikibot.pagegenerators import RecentChangesPageGenerator

from core.storage.updaters.lib.fetchers.base import BaseFetcher
from libs.utils.dt import dt


def reduce_seconds(dt):
    if not dt:
        return None
    return Timestamp(dt.year, dt.month, dt.day, dt.hour, dt.minute)


class RecentFetcher(BaseFetcher):
    slug = 'recent'

    def __init__(self, processor, namespaces, start=None, end=None):
        super().__init__(processor)
        self.namespaces = namespaces
        self.run(start, end)

    def run(self, start, end):
        start = reduce_seconds(start)
        end = reduce_seconds(end or self.processor.latest_edited)
        msg = f'Processing `recent` until: {dt(end)}'
        if start:
            msg += f' (starting from {dt(start)})'
        self.processor.log_day('cron', msg)
        generator = RecentChangesPageGenerator(start=start, end=end,
                                               namespaces=self.namespaces)
        latest_edited = None
        for page in generator:
            edited = self.processor.process_page(page)
            if not edited:
                continue
            latest_edited = latest_edited or reduce_seconds(edited)
        if latest_edited:
            self.processor.latest_edited = latest_edited
            self.processor.log_day('cron',
                                   f'New `latest_edited`: {dt(latest_edited)}')
