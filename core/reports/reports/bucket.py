from core.reports.reports.debug.divisible_length import DebugDivisibleLength
from core.reports.reports.headers.duplicated_first_level import \
    DuplicatedFirstLevel
from core.reports.reports.headers.duplicated_second_level import \
    DuplicatedSecondLevel
from core.reports.reports.headers.wrong_first_level import WrongFirstLevel
from core.reports.reports.headers.wrong_second_level import WrongSecondLevel
from core.reports.reports.ru.verbs.without_index import VerbsWithoutIndex
from core.reports.reports.ru.verbs.without_participles import \
    VerbsWithoutParticiples
from core.reports.reports.templates.key_duplicated import TemplateKeyDuplicated


class Bucket:
    _reports = {
        'recent': {},
        'all': {},
    }
    _reports_keys = []

    @classmethod
    def add(cls, reports_classes):
        for key in ['recent', 'all']:
            for report_class in reports_classes[key]:
                name = report_class.__name__
                if name in cls._reports_keys:
                    raise Exception(f'Report "{name}" already in a bucket.')
                cls._reports[key][name] = report_class()
                cls._reports_keys.append(name)

    @classmethod
    def get_reports(cls, only_recent=False):
        recent_reports = list(cls._reports['recent'].values())
        all_reports = list(cls._reports['all'].values())
        if only_recent:
            return recent_reports
        else:
            return recent_reports + all_reports

    @staticmethod
    def create_reports(reports_classes):
        reports = {}
        for report_class in reports_classes:
            name = report_class.__name__
            if name in reports:
                raise Exception(f'Duplicated report: "{name}".')
            reports[name] = report_class()
        return list(reports.values())


Bucket.add({
    'recent': [
        WrongFirstLevel,
        WrongSecondLevel,
        DuplicatedFirstLevel,
        DuplicatedSecondLevel,
        TemplateKeyDuplicated,
        VerbsWithoutIndex,
        # DebugDivisibleLength,
    ],
    'all': [
        VerbsWithoutParticiples,
    ]
})
