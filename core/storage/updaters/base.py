from pywikibot import NoPage

from core.storage.main import MainStorage
from libs.utils.dt import dt, t
from libs.utils.log import log_day, log_hour


class BaseStorageUpdater:
    """
    Обновление информации для хранилища.

    Примечание:
    Класс будет функционировать только во время работы конструктора,
    затем освобождает ресурсы (unlock для Storage)
    """
    def __init__(self, *args, **kwargs):
        """
        Примечание: В классах наследниках конструктор надо вызывать в хвосте
        """
        self.storage = MainStorage(lock=True)
        self.run(*args, **kwargs)
        self.storage.unlock()

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    def process_page(self, page):
        title = page.title()  # todo: except InvalidTitle ?
        self.log_day('titles', title)
        print(t(), title.encode('utf-8'), end=' ', flush=True)
        try:
            content = page.get(get_redirect=True)
            edited = page.editTime()
            redirect = page.isRedirectPage()
        except NoPage:
            self.storage.delete(title)
            print('- deleted')
            log_day('deleted.txt', title, path=self.storage.logs_path)
            return None

        edited_str = dt(edited, utc=True)
        info = f"{edited_str}, {'R' if redirect else 'A'}"
        self.storage.update(title, content=content, info=info)
        print('- updated:', edited_str)
        self.log_hour('changed', f'<{info}> - {title}')
        return edited

    def log_day(self, slug, value):
        log_day(slug, value, path=self.storage.logs_path)

    def log_hour(self, slug, value):
        log_hour(slug, value, path=self.storage.logs_path)
