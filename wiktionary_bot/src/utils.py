import time

import telegram
from telegram.error import BadRequest


def send(bot, chat_id, text, reply_markup=None, reply_to=None):
    return bot.send_message(chat_id=chat_id, text=text,
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.HTML,
                            disable_web_page_preview=True,
                            reply_to_message_id=reply_to)


def edit(bot, chat_id, msg_id, text, reply_markup=None):
    try:
        bot.edit_message_text(text=text, chat_id=chat_id,
                              message_id=msg_id,
                              reply_markup=reply_markup,
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)
        time.sleep(0.1)
        return True
    except BadRequest as e:
        if 'Message is not modified' in str(e):
            return False
        raise


def check_offensive(content):  # todo: move to utils
    offensives = ['{{off}}', '{{offensive}}', '{{Offensive}}']
    for offensive in offensives:
        if offensive in content:
            return True
    return False
