from core.storage.updaters.lib.fetchers.recent import RecentFetcher
from core.storage.updaters.lib.processors.storage import MainStorageProcessor
from libs.utils.log import log_exception
from libs.utils.wikibot import Namespace


@log_exception('updaters')
def update_recent_articles():
    RecentFetcher(MainStorageProcessor, [Namespace.ARTICLES])
