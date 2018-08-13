from projects.reports.lib.checkers.base import BaseChecker


class BaseSingleChecker(BaseChecker):
    def check(self, page):
        raise NotImplementedError()

    def build(self) -> list:
        return [self]
