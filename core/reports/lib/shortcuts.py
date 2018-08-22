from core.reports.lib.base import BaseIterableReport
from core.reports.lib.mixins.key_title import KeyTitle
from core.reports.lib.mixins.no_details import NoDetails


class TitlesReport(KeyTitle, NoDetails, BaseIterableReport):
    pass
