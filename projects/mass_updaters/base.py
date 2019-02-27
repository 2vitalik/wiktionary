import re

from libs.parse.online_page import OnlinePage
from libs.parse.storage_page import StoragePage
from libs.storage.error import PageNotFound
from libs.utils.classes import required
from libs.utils.dt import dt
from libs.utils.io import append
from libs.utils.wikibot import load_page, save_page


class MassUpdaterReport:
    def __init__(self, base):
        self.base = base
        self.lines = ''

    def error(self, title, value):
        line = self.process_line(f'[[{title}]]: ошибка, {value}', 'maroon')
        self.append('report/errors', line,
                    f'Ошибка в [[{title}]]: {value}')
        self.lines += line

    def success(self, title):
        self.lines += self.process_line(f'[[{title}]]: обработано', 'green')

    def status(self, value):
        self.lines += self.process_line(value, 'silver')
        self.save(value)

    def process_line(self, value, color):
        append(f'{self.base.slug}.txt', f'{dt()}: {value}')
        line = f'[{dt()}] {value}'
        if color == 'maroon':
            line = f'<b>{line}</b>'
        return f'* <span style="color: {color};">{line}</span>\n'

    def append(self, report_title, lines, desc):
        title = f"{self.base.data_page}/{report_title}"
        old_content = load_page(title, skip_absent=True)
        if not self.base.debug:
            save_page(title, f'{old_content}\n{lines}', desc)

    def save(self, desc):
        self.append('report', self.lines, desc)
        self.lines = ''


class BaseMassUpdater:
    slug = None
    data_page = None
    desc = None

    allow_several_lines = False

    def __init__(self, debug=False):
        self.debug = debug
        self.report = MassUpdaterReport(self)

    def check_entries(self, title, values):
        if len(values) > 1 and not self.allow_several_lines:
            self.report.error(title, 'ошибка, несколько строк на входе')
            return
        for value in values:
            if not self.check_entry(value):
                self.report.error(title, 'ошибка, формат записи в списке')
                return
        return True

    def check_entry(self, value):
        raise NotImplementedError()

    def process_page(self, page, title, values):
        raise NotImplementedError()

    @required('data_page', 'desc')
    def start(self):
        name = re.search(u':Cinemantique/(.+)', self.data_page).group(1)

        if f'* [[{self.data_page}|{name}]] = on' \
                not in load_page(u'User:Cinemantique/bot'):
            print(f'Bot `{self.data_page}` is offline.')
            return

        entries = load_page(self.data_page).strip().split('\n\n')
        if not entries:
            print(f'Page `{self.data_page}` is empty.')
            return

        self.report.status('Бот запущен')

        processed = []
        for i, entry in enumerate(entries):
            title, *values = entry.split('\n ')
            if not values:
                continue
            if not self.check_entries(title, values):
                continue
            if title in processed:
                self.report.error(title, 'дублируется в списке')
                continue
            processed.append(title)
            try:
                if self.debug:
                    page = StoragePage(title, silent=True)
                else:
                    page = OnlinePage(title, silent=True)
            except PageNotFound:
                self.report.error(title, 'в ВС нет статьи')
                continue
            if page.is_redirect:
                self.report.error(title, 'статья-редирект')
                continue
            if not page.ru:
                self.report.error(title, 'нет русского раздела в статье')
                continue
            if len(page.ru.homonyms.all()) > 1:
                self.report.error(title, 'омонимы в статье')

            if not self.process_page(page, title, values):
                continue

            try:
                if not self.debug:
                    page.upload_changes(self.desc)
            except Exception:
                self.report.error(title, 'что-то пошло не так')
                self.report.save('unexpected error')
                raise

            self.report.success(title)
            break

        self.report.status('Бот завершён')

        if not self.debug:
            desc = f'Готово: [[{self.data_page}/report|отчёт]]'
            save_page(self.data_page, '', desc)
