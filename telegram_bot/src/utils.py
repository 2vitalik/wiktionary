import telegram


def send(bot, chat_id, text, reply_markup=None):
    bot.send_message(chat_id=chat_id, text=text,
                     reply_markup=reply_markup,
                     parse_mode=telegram.ParseMode.HTML,
                     disable_web_page_preview=True)
