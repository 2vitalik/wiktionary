from core.reports.lib.shortcuts import TitlesReport


class DebugDivisibleLength(TitlesReport):
    path = 'Temp/Просто для отладки некоторых процессов'
    description = '''
        Этот отчёт не несёт никакого смысла, кроме как для генерации некоторых 
        списков для отладки и сравнения нескольких разных процессов обновления 
        отчётов.
    '''

    def check_page(self, page) -> bool:
        return len(page.content) % 1500 == 0

    def convert_entries(self):
        self.entries = dict(sorted(self.entries.items(), key=lambda x: x[0]))
