from collections import defaultdict

from core.reports.lib.large_report.base import BaseLargeReport
from libs.utils.unicode import unicode_sorted_key


class FirstLetterLargeReport(BaseLargeReport):
    def group_entries(self):
        grouped = defaultdict(list)
        for title in self.entries:
            letter = title[0].upper()
            grouped[letter].append(title)

        # todo: use ALL LETTERS optionally?
        return dict(sorted(grouped.items(),
                           key=lambda x: unicode_sorted_key(x[0])))
