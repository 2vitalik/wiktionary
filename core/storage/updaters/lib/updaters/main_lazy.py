from shared_utils.api.slack.core import post_to_slack

from core.storage.updaters.lib.updaters.main import MainStorageUpdater
from libs.utils.dt import dt


class LazyMainStorageUpdater(MainStorageUpdater):
    """
    Обновление информации в главном хранилище *только* при необходимости.
    """
    def update_page(self, title, content, edited, redirect):
        old_content, old_info = self.storage.get(title, silent=True)

        edited_str = dt(edited, utc=True)
        info = f"{edited_str}, {'R' if redirect else 'A'}"

        if content != old_content or info != old_info:
            self.storage.update(title, content=content, info=info)
            self.log_hour('changed', f'<{info}> - {title}')
            self.log_day('titles_changed', title)
            icon = '🔸' if redirect else '🔹'
            msg = f'{icon} _{edited_str}_ — ' \
                f'*<https://ru.wiktionary.org/wiki/{title}|{title}>*'
            post_to_slack(f'{self.slug}-changed', msg)
