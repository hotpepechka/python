import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Установите уровень логирования, чтобы видеть информацию о запросах и ошибках
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
START, FIRST_REPLY = range(2)


# Функция, которая будет вызываться при команде /start
def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_html(
        fr"Привет, {user.mention_html()}!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return FIRST_REPLY


# Функция, которая будет вызываться при получении текстового сообщения от пользователя
def reply_text(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    text = update.message.text
    update.message.reply_html(
        fr"Спасибо за ваше сообщение: {text}",
        reply_markup=ReplyKeyboardRemove(),
    )

    return FIRST_REPLY


# Функция, которая будет вызываться при команде /cancel
def cancel(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_html(
        fr"До свидания, {user.mention_html()}!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def main():
    #'' = token из tg
    updater = Updater(token='', use_context=True)

    dp = updater.dispatcher

    # Добавьте хендлеры команд /start и /cancel
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_REPLY: [MessageHandler(Filters.text & ~Filters.command, reply_text)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # Запускаем бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
