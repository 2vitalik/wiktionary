from core.reports.lib.large_report.first_letter import FirstLetterLargeReport
from core.reports.lib.large_report.plurals import PluralVerbs
from core.reports.lib.shortcuts import TitlesReport


class VerbsWithoutIndex(TitlesReport, PluralVerbs, FirstLetterLargeReport):
    path = 'Отчёты/ru/Глаголы/Без классификации по Зализняку'
    short_title = 'Глаголы без классификации по Зализняку'

    def get_short_title(self, letter):
        return f'Глаголы на «{letter}» без классификации по Зализняку'

    def check_page(self, page) -> bool:
        return page.ru and page.data.ru.has_unindexed_verb()
