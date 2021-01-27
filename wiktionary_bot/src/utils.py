import time

import telegram
from telegram.error import BadRequest


def send(bot, chat_id, text, reply_markup=None):
    return bot.send_message(chat_id=chat_id, text=text,
                            reply_markup=reply_markup,
                            parse_mode=telegram.ParseMode.HTML,
                            disable_web_page_preview=True)


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
