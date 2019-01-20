from core.storage.updaters.lib.fetchers.all import AllPagesFetcher
from core.storage.updaters.lib.fetchers.recent import RecentFetcher
from core.storage.updaters.lib.updaters.main_lazy import LazyMainStorageUpdater
# from core.storage.updaters.lib.updaters.sync import SyncUpdater
from libs.utils.log import log_exception
from libs.utils.wikibot import Namespace


@log_exception('updaters')
def update_recent_articles():
    RecentFetcher(LazyMainStorageUpdater, [Namespace.ARTICLES])


@log_exception('updaters')
def update_all_articles(stopper=None):
    AllPagesFetcher(LazyMainStorageUpdater, [Namespace.ARTICLES], stopper)
