from core.storage.updaters.lib.fetchers.recent import RecentFetcher
from core.storage.updaters.lib.processors.storage import MainStorageProcessor
from libs.utils.wikibot import Namespace


def recent_articles():
    RecentFetcher(MainStorageProcessor(), [Namespace.ARTICLES])
