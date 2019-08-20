import sys; sys.path.append('../..')
from datetime import datetime
from os.path import join

import telegram
from pywikibot import Timestamp, NoPage
from pywikibot.pagegenerators import RecentChangesPageGenerator

from libs.parse.sections.page import Page
from libs.utils.io import write, read, read_lines, append
from libs.utils.wikibot import Namespace
from telegram_bot.config import TELEGRAM_BOT_TOKEN, ROOT_PATH, NEW_CHANNEL_ID
from telegram_bot.src.semantic import Reply
from telegram_bot.src.utils import send


def convert_date(value):
    if not value:
        return None
    return Timestamp(value.year, value.month, value.day,
                     value.hour, value.minute, value.second)


def latest_date_file():
    return join(ROOT_PATH, 'telegram_bot', 'data', 'latest_new_article.txt')


def get_latest_date():
    return convert_date(datetime.strptime(read(latest_date_file()).strip(),
                                          '%Y-%m-%d %H:%M:%S'))


def set_latest_date(value):
    write(latest_date_file(), value.strftime('%Y-%m-%d %H:%M:%S'))


def titles_file():
    return join(ROOT_PATH, 'telegram_bot', 'data', 'titles.txt')


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
        print(title, '- ', end='')
        try:
            content = page.get(get_redirect=True)
            edited = page.editTime()
            print(edited)
        except NoPage:
            print('None')
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
        if Page(title, content).ru:
            new_titles.append(title)
            print('- NEW!', '*' * 100)
    if latest_edited:
        set_latest_date(latest_edited)
    return new_titles


if __name__ == '__main__':
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    new_titles = get_new_articles()
    print(new_titles)
    chat_id = NEW_CHANNEL_ID
    for title in reversed(new_titles):
        send(bot, chat_id, Reply(title).text)
        append_title(title)


# todo: update current messages if they updates on Wiktionary?
