import up  # don't remove this
from core.storage.postponed.shortcuts import update_recent
from core.storage.updaters.lib.fetchers.all import MinuteStopper
from core.storage.updaters.shortcuts import update_recent_articles, \
    update_all_articles


if __name__ == '__main__':
    update_recent_articles()
    # update_recent('authors')  # todo: process slack errors
    # todo: update_recent_sync()
    update_all_articles(MinuteStopper(59))
