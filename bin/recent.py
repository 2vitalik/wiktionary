import up
from core.storage.updaters.lib.fetchers.all import MinuteStopper
from core.storage.updaters.shortcuts import update_recent_articles, \
    update_all_articles


if __name__ == '__main__':
    update_recent_articles()
    # todo: update_recent_sync()
    update_all_articles(MinuteStopper(59))
