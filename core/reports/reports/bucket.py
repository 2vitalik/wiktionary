from core.reports.reports.debug.divisible_length import DebugDivisibleLength
from core.reports.reports.headers.duplicated_first_level import \
    DuplicatedFirstLevel
from core.reports.reports.headers.duplicated_second_level import \
    DuplicatedSecondLevel
from core.reports.reports.headers.wrong_first_level import WrongFirstLevel
from core.reports.reports.headers.wrong_second_level import WrongSecondLevel
from core.reports.reports.ru.verbs.without_participles import \
    VerbsWithoutParticiples


class Bucket:
    reports = {}

    @classmethod
    def add(cls, *reports):
        for report in reports:
            name = report.__name__
            if name in cls.reports:
                raise Exception(f'Report {name} already in a bucket.')
            cls.reports[name] = report()


Bucket.add(
    WrongFirstLevel,
    WrongSecondLevel,
    DuplicatedFirstLevel,
    DuplicatedSecondLevel,
    VerbsWithoutParticiples,
    DebugDivisibleLength,
)
