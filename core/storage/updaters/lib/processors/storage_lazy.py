from core.storage.updaters.lib.processors.storage import MainStorageProcessor
from libs.utils.dt import dt


class LazyMainStorageProcessor(MainStorageProcessor):
    """
    Обновление информации в главном хранилище *только* при необходимости.
    """
    def process_update(self, title, content, edited, redirect):
        old_content, old_info = self.storage.get(title)

        edited_str = dt(edited, utc=True)
        info = f"{edited_str}, {'R' if redirect else 'A'}"

        if content != old_content or info != old_info:
            self.storage.update(title, content=content, info=info)
            self.log_hour('changed', f'<{info}> - {title}')
