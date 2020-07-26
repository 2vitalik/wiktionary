from core.reports.lib.large_report.first_letter import FirstLetterLargeReport
from core.reports.lib.large_report.plurals import PluralVerbs
from core.reports.lib.shortcuts import TitlesReport


class VerbsWithoutTranscription(TitlesReport, PluralVerbs,
                                FirstLetterLargeReport):
    path = 'Отчёты/ru/Глаголы/Без транскрипции'
    short_title = 'Глаголы без транскрипции'

    def get_short_title(self, letter):
        return f'Глаголы на «{letter}» без транскрипции'

    def check_page(self, page) -> bool:
        return page.ru and page.data.ru.has_untranscribed_verb()
