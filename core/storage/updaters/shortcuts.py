from core.storage.updaters.lib.fetchers.all import AllPagesFetcher
from core.storage.updaters.lib.fetchers.recent import RecentFetcher
from core.storage.updaters.lib.processors.main_lazy import \
    LazyMainStorageProcessor
from libs.utils.log import log_exception
from libs.utils.wikibot import Namespace


@log_exception('updaters')
def update_recent_articles():
    RecentFetcher(LazyMainStorageProcessor, [Namespace.ARTICLES])


@log_exception('updaters')
def update_all_articles(stopper=None):
    AllPagesFetcher(LazyMainStorageProcessor, [Namespace.ARTICLES], stopper)
