from pywikibot import Timestamp
from pywikibot.pagegenerators import RecentChangesPageGenerator
from shared_utils.api.slack.core import post_to_slack

from core.storage.updaters.lib.fetchers.base import BaseFetcher
from libs.utils.dt import dt


def reduce_seconds(value):
    if not value:
        return None
    return Timestamp(value.year, value.month, value.day,
                     value.hour, value.minute)


class RecentFetcher(BaseFetcher):
    slug = 'recent'

    def __init__(self, updater_class, namespaces, start=None, end=None):
        """
        :param updater_class: subclass of BaseUpdater
        :param namespaces: list of pywikibot namespaces
        """
        super().__init__(updater_class)
        self.namespaces = namespaces
        self.run(start, end)
        self.updater.close()

    def run(self, start, end):
        start = reduce_seconds(start)
        end = reduce_seconds(end or self.updater.latest_edited)
        msg = f':rocket: Started at *{dt(end)}*'
        if start:
            msg += f' (starting from {dt(start)})'
        self.updater.log_day('cron', msg)
        post_to_slack(f'{self.slug}-status', msg)
        generator = RecentChangesPageGenerator(start=start, end=end,
                                               namespaces=self.namespaces)
        latest_edited = None
        for page in generator:
            title, edited = self.updater.process_page(page)
            if not edited:
                continue
            latest_edited = latest_edited or reduce_seconds(edited)
        if latest_edited:
            self.updater.latest_edited = latest_edited
            msg = f':white_check_mark: Finished at *{dt(latest_edited)}*'
            self.updater.log_day('cron', msg)
            post_to_slack(f'{self.slug}-status', msg)
