from projects.reports.reports.headers.duplicated_first_level import \
    DuplicatedFirstLevel
from projects.reports.reports.headers.wrong_first_level import WrongFirstLevel
from projects.reports.reports.headers.wrong_second_level import WrongSecondLevel
from projects.reports.reports.ru.verbs.without_participles import \
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
    VerbsWithoutParticiples,
    WrongFirstLevel,
    WrongSecondLevel,
    DuplicatedFirstLevel,
)
