import sys; sys.path.append('../..')
from datetime import datetime
from os.path import join

import telegram
from pywikibot import Timestamp, NoPage
from pywikibot.pagegenerators import RecentChangesPageGenerator

from core.conf import conf
from libs.parse.sections.page import Page
from libs.utils.io import write, read, read_lines, append
from libs.utils.lock import locked_repeat
from libs.utils.wikibot import Namespace
from wiktionary_bot.cron.bots import bots
from wiktionary_bot.src.semantic import Reply, get_author
from wiktionary_bot.src.utils import send


def convert_date(value):
    if not value:
        return None
    return Timestamp(value.year, value.month, value.day,
                     value.hour, value.minute, value.second)


class latest_date:
    filename = join(conf.data_path, 'new_articles', 'latest_new_article.txt')

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


def get_new_articles():
    old_titles = titles.get()
    new_titles = []
    start = None
    # start = datetime(2021, 1, 24, 13, 50)  # just for debug
    generator = \
        RecentChangesPageGenerator(start=start, end=latest_date.get(),
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
        latest_date.set(latest_edited)
    return new_titles


@locked_repeat('new_articles')
def run():
    bot = telegram.Bot(conf.telegram_token)
    new_titles = get_new_articles()
    chat_id = conf.new_channel_id
    for title in reversed(new_titles):
        reply = Reply(title)
        text = reply.text + get_author(title)
        if '🔻 Секция «Семантические свойства» не найдена' not in reply.text:
            send(bot, chat_id, text, reply_markup=reply.buttons)
        titles.add(title)


if __name__ == '__main__':
    run()


# todo: update current messages if they updates on Wiktionary?
