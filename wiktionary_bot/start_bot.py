import sys; sys.path.append('..')
import logging

from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from shared_utils.conf import conf as shared_conf

from wiktionary_bot import config
from wiktionary_bot.src.semantic import process_message, process_callback
from wiktionary_bot.src.slack import slack_status


def start():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s (%(name)s):  %(message)s'
    )
    shared_conf.slack_hooks = config.slack_hooks

    bot = Bot(config.TELEGRAM_BOT_TOKEN)
    bot.send_message(config.TELEGRAM_ADMIN, '💬 Starting the bot...')
    slack_status('💬 Starting the bot...')

    updater = Updater(token=config.TELEGRAM_BOT_TOKEN)
    d = updater.dispatcher

    d.add_handler(MessageHandler(Filters.text, process_message))
    d.add_handler(CallbackQueryHandler(process_callback))

    updater.start_polling()
    print('Bot has successfully started.')
    updater.idle()


if __name__ == '__main__':
    start()
