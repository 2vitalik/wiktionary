
class BaseFetcher:
    slug = None  # should be set in inheritors

    def __init__(self, updater_class):
        self.updater = updater_class(self.slug)
