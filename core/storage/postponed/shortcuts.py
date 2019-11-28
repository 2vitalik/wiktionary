from libs.utils.log import log_exception


def get_class(key):

    if type(key) == str:
        if key == 'authors':
            from projects.authors.authors_updater import AuthorsStorageUpdater
            return AuthorsStorageUpdater
        elif key == 'htmls':
            from projects.htmls.htmls_updater import HtmlStorageUpdater
            return HtmlStorageUpdater

    return key  # if we just use certain class here


def update_recent(key):

    @log_exception(key)
    def wrapped():
        cls = get_class(key)
        cls().run()

    wrapped()


def update_all(key):

    @log_exception(key)
    def wrapped():
        cls = get_class(key)
        cls(process_all=True).run()

    wrapped()
