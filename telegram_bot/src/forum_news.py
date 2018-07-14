import json
import re
from os.path import exists, join

import telegram

from lib.utils.wikibot import load_page
from telegram_bot.config import TELEGRAM_BOT_TOKEN, ROOT_PATH, \
    MAIN_GROUP_CHAT_ID
from telegram_bot.src.utils import send


forums = [
    'Викисловарь:Портал сообщества',
    'Викисловарь:Лингвистические и лексикографические вопросы',
    'Викисловарь:Организационные вопросы',
    'Викисловарь:Технические вопросы',
    'Викисловарь:Вопросы общения',
    'Викисловарь:Лицензионные вопросы',
    'Викисловарь:Работа для бота',
]


def check_for_new_titles(bot):
    old_data = {}
    new_data = {}

    json_path = join(ROOT_PATH, 'telegram_bot', 'data', 'forums.json')
    if exists(json_path):
        with open(json_path, encoding='utf-8') as f:
            old_data = json.load(f)

    for forum in forums:
        content = load_page(forum)
        titles = re.findall('^==(.*)==$', content, re.MULTILINE)
        titles = list(map(str.strip, titles))
        new_data[forum] = titles
        old_titles = old_data.get(forum, [])
        new_titles = list(set(titles) - set(old_titles))
        if new_titles:
            forum_name = forum[len('Викисловарь:'):]
            message_text = f'📝 <b>Новая тема на форуме!</b>\n' \
                           f'«{forum_name}»\n'
            for title in new_titles:
                title = title.replace('<', '&lt;')
                title = title.replace('>', '&gt;')
                title = title.strip('=').strip()
                link = f'→ <a href="https://ru.wiktionary.org/wiki/{forum}">' \
                       f'{title}</a>\n'
                message_text += link
            # chat_id = DEV_CHAT_ID
            chat_id = MAIN_GROUP_CHAT_ID
            send(bot, chat_id, message_text)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4)


if __name__ == '__main__':
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    check_for_new_titles(bot)
