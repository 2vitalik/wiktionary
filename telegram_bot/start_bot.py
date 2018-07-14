import logging

from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler

from telegram_bot.config import TELEGRAM_BOT_TOKEN
from telegram_bot.src.semantic import process_message, process_callback


def start():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s (%(name)s):  %(message)s'
    )
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, process_message))
    dispatcher.add_handler(CallbackQueryHandler(process_callback))
    updater.start_polling()
    print('Bot has successfully started.')
    updater.idle()


if __name__ == '__main__':
    start()
