import sys; sys.path.append('../..')
from datetime import datetime
from os.path import join

import telegram
from pywikibot import Timestamp, NoPage
from pywikibot.pagegenerators import RecentChangesPageGenerator

from libs.parse.sections.page import Page
from libs.utils.io import write, read, read_lines, append
from libs.utils.wikibot import Namespace
from wiktionary_bot.config import TELEGRAM_BOT_TOKEN, NEW_CHANNEL_ID, data_path
from wiktionary_bot.cron.bots import bots
from wiktionary_bot.src.semantic import Reply
from wiktionary_bot.src.utils import send


def convert_date(value):
    if not value:
        return None
    return Timestamp(value.year, value.month, value.day,
                     value.hour, value.minute, value.second)


def latest_date_file():
    return join(data_path, 'new_articles', 'latest_new_article.txt')


def get_latest_date():
    return convert_date(datetime.strptime(read(latest_date_file()).strip(),
                                          '%Y-%m-%d %H:%M:%S'))


def set_latest_date(value):
    write(latest_date_file(), value.strftime('%Y-%m-%d %H:%M:%S'))


def titles_file():
    return join(data_path, 'new_articles', 'titles.txt')


def get_titles_set():
    return set(read_lines(titles_file()))


def append_title(title):
    append(titles_file(), title)


def get_new_articles():
    old_titles = get_titles_set()
    new_titles = []
    generator = \
        RecentChangesPageGenerator(end=get_latest_date(),
                                   namespaces=[Namespace.ARTICLES])
    latest_edited = None
    for page in generator:
        title = page.title()
        try:
            content = page.get(get_redirect=True)
            edited = page.editTime()
            user = page.userName()
            if user in bots:
                continue
        except NoPage:
            continue
        latest_edited = latest_edited or convert_date(edited)
        if title in new_titles:
            continue
        if title in old_titles:
            continue
        has_offensive = False
        offensives = ['{{off}}', '{{offensive}}', '{{Offensive}}']
        for offensive in offensives:
            if offensive in content:
                has_offensive = True
        if has_offensive:
            continue
        if Page(title, content, silent=True).ru:
            new_titles.append(title)
    if latest_edited:
        set_latest_date(latest_edited)
    return new_titles


if __name__ == '__main__':
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    new_titles = get_new_articles()
    chat_id = NEW_CHANNEL_ID
    for title in reversed(new_titles):
        reply = Reply(title)
        if '🔻 Секция «Семантические свойства» не найдена' not in reply.text:
            send(bot, chat_id, reply.text, reply_markup=reply.buttons)
        append_title(title)


# todo: update current messages if they updates on Wiktionary?
