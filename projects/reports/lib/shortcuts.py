from projects.reports.lib.base import BaseIterableReport
from projects.reports.lib.mixins.key_title import KeyTitle
from projects.reports.lib.mixins.no_details import NoDetails


class TitlesReport(KeyTitle, NoDetails, BaseIterableReport):
    pass
