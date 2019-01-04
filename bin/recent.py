import up  # don't remove this
from core.storage.updaters.lib.fetchers.all import MinuteStopper
from core.storage.updaters.shortcuts import update_recent_articles, \
    update_all_articles
from projects.authors.authors_processor import update_recent_authors


if __name__ == '__main__':
    update_recent_articles()
    update_recent_authors()
    # todo: update_recent_sync()
    update_all_articles(MinuteStopper(59))
