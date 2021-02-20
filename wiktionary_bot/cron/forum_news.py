import sys; sys.path.append('../..')
import json
import re
from os.path import exists, join

import telegram

from core.conf import conf
from libs.utils.wikibot import load_page
from wiktionary_bot.src.slack import slack
from wiktionary_bot.src.utils import send


forums = [
    'Викисловарь:Общие вопросы',
    'Викисловарь:Лингвистические и лексикографические вопросы',
    'Викисловарь:Организационные вопросы',
    'Викисловарь:Технические вопросы',
    'Викисловарь:Вопросы общения',
    'Викисловарь:Лицензионные вопросы',
    'Викисловарь:Работа для бота',
]


@slack('forum_news')
def check_for_new_titles(bot):
    old_data = {}
    new_data = {}

    json_path = join(conf.data_path, 'forum_news', 'forums.json')
    if exists(json_path):
        with open(json_path, encoding='utf-8') as f:
            old_data = json.load(f)

    for forum in forums:
        old_titles = old_data.get(forum, [])

        content = load_page(forum)
        titles = re.findall('^==(.*)==\s*$', content, re.MULTILINE)
        titles = list(map(str.strip, titles))
        new_data[forum] = titles

        new_titles = []
        for title in titles:
            if title not in old_titles:
                new_titles.append(title)

        if new_titles:
            forum_name = forum[len('Викисловарь:'):]
            message_text = f'📝 <b>Новая тема на форуме!</b>\n' \
                           f'«{forum_name}»\n'
            for title in new_titles:
                title = title.replace('<', '&lt;')
                title = title.replace('>', '&gt;')
                title = title.strip('=').strip()
                forum = forum.replace(' ', '_')
                link = f'→ <a href="https://ru.wiktionary.org/wiki/{forum}">' \
                       f'{title}</a>\n'
                message_text += link
            # chat_id = DEV_CHAT_ID
            chat_id = conf.main_group_id
            send(bot, chat_id, message_text)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4)


if __name__ == '__main__':
    bot = telegram.Bot(conf.telegram_token)
    check_for_new_titles(bot)
