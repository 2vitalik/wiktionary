from libs.utils.classes import required
from libs.utils.log import log_day, log_hour


class LogsMixin:
    slug = None  # should be set in inheritor

    @property
    def logs_path(self):
        raise NotImplementedError()

    @required('slug')
    def log_day(self, sub_slug, value):
        log_day(f"{self.slug}/{sub_slug}", value, path=self.logs_path)

    @required('slug')
    def log_hour(self, sub_slug, value):
        log_hour(f"{self.slug}/{sub_slug}", value, path=self.logs_path)


class StorageLogsMixin(LogsMixin):
    storage = None  # should be set in inheritor

    @property
    def logs_path(self):
        return self.storage.logs_path
