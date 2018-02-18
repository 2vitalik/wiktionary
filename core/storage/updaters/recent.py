from pywikibot import Timestamp
from pywikibot.pagegenerators import RecentChangesPageGenerator

from core.storage.updaters.base import BaseStorageUpdater


def reduce_seconds(dt):
    return Timestamp(dt.year, dt.month, dt.day, dt.hour, dt.minute)


class RecentStorageUpdater(BaseStorageUpdater):
    def __init__(self, start=None, end=None):
        super().__init__()
        start = reduce_seconds(start)
        end = reduce_seconds(end or self.storage.latest_edited)
        generator = \
            RecentChangesPageGenerator(start=start, end=end, namespaces=[0])

        latest_edited = None
        for page in generator:
            edited = self.process_page(page)
            if not edited:
                continue
            latest_edited = latest_edited or reduce_seconds(edited)
        if latest_edited:
            self.storage.latest_edited = latest_edited