from projects.reports.lib.base import BaseIterableReport


class ReversedIndex(BaseIterableReport):
    def convert_entries(self):
        self.entries = dict(sorted(self.entries.items(),
                                   key=lambda x: x[0][::-1]))
