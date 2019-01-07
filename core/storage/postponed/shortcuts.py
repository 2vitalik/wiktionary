from libs.utils.log import log_exception


def get_class(key):
    from projects.authors.authors_updater import AuthorsStorageUpdater
    from projects.htmls.htmls_updater import HtmlStorageUpdater

    if type(key) == str:
        classes = {
            'authors': AuthorsStorageUpdater,
            'htmls': HtmlStorageUpdater,
        }
        return classes[key]

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
