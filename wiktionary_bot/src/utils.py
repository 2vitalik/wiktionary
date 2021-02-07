import time

import telegram
from telegram.error import BadRequest, TimedOut, RetryAfter

from wiktionary_bot.src.slack import slack_error, add_quote


def send(bot, chat_id, text, reply_markup=None, reply_to=None, pause=1):
    try:
        return bot.send_message(chat_id=chat_id, text=text,
                                reply_markup=reply_markup,
                                parse_mode=telegram.ParseMode.HTML,
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_to)
    except (TimedOut, RetryAfter) as e:  # todo: join common part between `send` and `edit` and move to shared utils
        print(f'TimedOut or RetryAfter Error: Pause for {pause} seconds...')
        slack_error(f'`send`  *{type(e).__name__}*: {str(e)}\n\n'
                    f'Pause for {pause} seconds...\n\n'
                    f'>chat_id: {chat_id}\n\n'
                    f'>{add_quote(text)}')
        time.sleep(pause)
        return send(bot, chat_id, text, reply_markup, reply_to, pause * 2)


def edit(bot, chat_id, msg_id, text, reply_markup=None, pause=1):
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
    except (TimedOut, RetryAfter) as e:  # todo: join common part between `send` and `edit` and move to shared utils
        print(f'TimedOut or RetryAfter Error: Pause for {pause} minute...')
        slack_error(f'`edit`  *{type(e).__name__}*: {str(e)}\n\n'
                    f'Pause for {pause} minute...\n\n'
                    f'>chat_id: {chat_id}\n\n'
                    f'>{add_quote(text)}')
        time.sleep(pause)
        return edit(bot, chat_id, text, reply_markup, pause * 2)


def check_offensive(content):  # todo: move to utils
    offensives = ['{{off}}', '{{offensive}}', '{{Offensive}}']
    for offensive in offensives:
        if offensive in content:
            return True
    return False
