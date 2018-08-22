from os.path import join, exists

from libs.utils.dt import dtp, dt
from libs.utils.io import read, write


class UpdatersValuesMixin:
    @property
    def latest_edited_filename(self):
        return join(self.path, 'sys', 'latest_edited')

    @property
    def latest_edited(self):
        if not exists(self.latest_edited_filename):
            return None
        return dtp(read(self.latest_edited_filename))

    @latest_edited.setter
    def latest_edited(self, value):
        write(self.latest_edited_filename, dt(value, utc=True))

    @property
    def all_pages_start_from_filename(self):
        return join(self.path, 'sys', 'all_pages_start_from')

    @property
    def all_pages_start_from(self):
        if not exists(self.all_pages_start_from_filename):
            return None
        return read(self.all_pages_start_from_filename)

    @all_pages_start_from.setter
    def all_pages_start_from(self, value):
        write(self.all_pages_start_from_filename, value)


class PostponedValuesMixin:
    @property
    def latest_updated_filename(self):
        return join(self.path, 'sys', 'latest_updated')

    @property
    def latest_updated(self):
        if not exists(self.latest_updated_filename):
            return None
        return dtp(read(self.latest_updated_filename))

    @latest_updated.setter
    def latest_updated(self, value):
        write(self.latest_updated_filename, dt(value, utc=True))
