import sys; sys.path.append('../..')
from datetime import datetime

import telegram

from core.conf import conf
from libs.utils.io import json_load
from wiktionary_bot.src.semantic import Reply
from wiktionary_bot.src.slack import slack
from wiktionary_bot.src.utils import send


@slack('send_daily_word')
def send_daily_word():
    bot = telegram.Bot(conf.telegram_token)
    chat_id = conf.new_channel_id

    now = datetime.now()
    year_month = now.strftime('%Y/%m')
    path = f'{conf.data_path}/word_of_day/{year_month}/latest.json'
    data = json_load(path)
    title = data[str(now.day)]
    print(title)

    text = '🔆 Слово дня\n' + Reply(title).text
    send(bot, chat_id, text)


if __name__ == '__main__':
    send_daily_word()
