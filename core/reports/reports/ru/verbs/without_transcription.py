from core.reports.lib.large_report.first_letter import FirstLetterLargeReport
from core.reports.lib.large_report.plurals import PluralVerbs
from core.reports.lib.shortcuts import TitlesReport
from libs.parse.storage_page import StoragePage


class VerbsWithoutTranscription(TitlesReport, PluralVerbs,
                                FirstLetterLargeReport):
    path = 'Отчёты/ru/Глаголы/Без транскрипции'
    short_title = 'Глаголы без транскрипции'

    def get_short_title(self, letter):
        return f'Глаголы на «{letter}» без транскрипции'

    def check_page(self, page) -> bool:
        return page.ru and page.data.ru.has_untranscribed_verb()


if __name__ == '__main__':
    page = StoragePage('обвозиться')
    print(VerbsWithoutTranscription().check_page(page))
