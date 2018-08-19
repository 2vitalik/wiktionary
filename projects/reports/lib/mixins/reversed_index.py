from projects.reports.lib.base import BaseIterableReport


class ReversedIndex(BaseIterableReport):
    def convert_entries(self):
        new_entries = {}
        for key, value in sorted(self.entries.items(), key=lambda x: x[0][::-1]):
            new_entries[key] = value
        self.entries = new_entries
