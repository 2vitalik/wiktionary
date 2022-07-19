import sys; sys.path.append('../..')
from datetime import datetime
from os.path import join

import telegram
from pywikibot import Timestamp, NoPage
from pywikibot.pagegenerators import RecentChangesPageGenerator, \
    LogeventsPageGenerator

from core.conf import conf
from libs.parse.sections.page import Page
from libs.utils.io import write, read, read_lines, append, json_load, json_dump
from libs.utils.lock import locked_repeat
from libs.utils.wikibot import Namespace
from wiktionary_bot.cron.bots import bots
from wiktionary_bot.src.semantic import Reply, get_author
from wiktionary_bot.src.slack import slack_status, slack_error, slack
from wiktionary_bot.src.utils import send, edit, check_offensive


def convert_date(value):
    if not value:
        return None
    return Timestamp(value.year, value.month, value.day,
                     value.hour, value.minute, value.second)


class latest_date:
    filename = join(conf.data_path, 'new_articles', 'latest_processed.txt')

    @classmethod
    def get(cls):
        return convert_date(datetime.strptime(read(cls.filename).strip(),
                                              '%Y-%m-%d %H:%M:%S'))

    @classmethod
    def set(cls, value):
        write(cls.filename, value.strftime('%Y-%m-%d %H:%M:%S'))


class titles:
    filename = join(conf.data_path, 'new_articles', 'titles.txt')

    @classmethod
    def get(cls):
        return set(read_lines(cls.filename))

    @classmethod
    def add(cls, title):
        append(cls.filename, title)


class messages:
    filename = join(conf.data_path, 'new_articles', 'messages.json')
    ids = json_load(filename)

    @classmethod
    def get(cls, title):
        return cls.ids[title]

    @classmethod
    def set(cls, title, message_id):
        if title in cls.ids:
            slack_error(f'⚠️ Сообщение для "`{title}`" уже было?')
        cls.ids[title] = message_id
        json_dump(cls.filename, cls.ids)


def get_new_articles():
    old_titles = titles.get()
    new_titles = []
    changed_titles = set()
    deleted_titles = set()

    # info: check for deleted pages:
    # print('LogeventsPageGenerator')
    generator = LogeventsPageGenerator(
        # start=datetime(2021, 1, 27, 3, 30),  # info: just for debug
        end=latest_date.get(),
        namespace=Namespace.ARTICLES,
    )
    for page in generator:
        title = page.title()
        print(title)
        try:
            page.get(get_redirect=True)
        except NoPage:
            deleted_titles.add(title)
            continue

    # info: check for created and edited pages:
    generator = RecentChangesPageGenerator(
        # start=datetime(2021, 1, 26, 23, 00),  # info: just for debug
        end=latest_date.get(),
        namespaces=[Namespace.ARTICLES],
    )
    print('RecentChangesPageGenerator')
    slack_status(f'RecentChangesPageGenerator')
    latest_processed = None
    for page in generator:
        title = page.title()
        print(title)
        try:
            content = page.get(get_redirect=True)
            edited = page.editTime()
            latest_processed = latest_processed or convert_date(edited)
            # print(edited, title)  # info: just for debug
            user = page.userName()
            if user in bots:
                continue
        except NoPage:  # info: probably will never happen here
            deleted_titles.add(title)
            continue
        if title in new_titles:
            continue
        if title in changed_titles:
            continue
        if title in old_titles:
            if title in messages.ids:
                changed_titles.add(title)
            continue
        if check_offensive(content):
            continue

        if Page(title, content, silent=True).ru:
            new_titles.append(title)

    if latest_processed:
        latest_date.set(latest_processed)
    print('finished')
    slack_status(f'Finishing...')
    return new_titles, changed_titles, deleted_titles


@locked_repeat('new_articles')
@slack('new_articles')
def process_new_articles():
    slack_status(f'Starting...')
    bot = telegram.Bot(conf.telegram_token)
    new_titles, changed_titles, deleted_titles = get_new_articles()
    chat_id = conf.new_channel_id
    # print('sending...')
    for title in reversed(new_titles):
        reply = Reply(title)
        text = reply.text + get_author(title)
        text = text.replace('   <i>// русский</i>', '')
        if '🔻 Секция «Семантические свойства» не найдена' not in reply.text:
            msg = send(bot, chat_id, text)
            messages.set(title, msg.message_id)
        titles.add(title)
    # print('changing...')
    for title in changed_titles:
        message_id = messages.ids[title]
        reply = Reply(title)
        text = reply.text + get_author(title)
        text = text.replace('   <i>// русский</i>', '')
        if '🔻 Секция «Семантические свойства» не найдена' not in reply.text:
            if edit(bot, chat_id, message_id, text):
                slack_status(f'✏️ Сообщение для "`{title}`" было обновлено')
    # print('deleting...')
    for title in deleted_titles:
        if title in messages.ids:
            message_id = messages.ids[title]
            removed_message = \
                f'🙅🏻‍♂️ Статья "{title}" была удалена из Викисловаря'
            if edit(bot, chat_id, message_id, removed_message):
                slack_status(f'❌️ Сообщение для "`{title}`" было "удалено"')


if __name__ == '__main__':
    process_new_articles()
