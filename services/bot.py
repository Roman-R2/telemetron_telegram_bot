import telebot

from services.telemetron import TelemetronRequests
from settings import settings

bot = telebot.TeleBot(settings.TELEGRAM_API_TOKEN)

telemetron = TelemetronRequests()


# Handle '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "/need - Покажет какие ингредиенты нужно взять с собой\n/capacity - Покажет текущую загрузку по всем автоматам "
    )


# Handle '/need'
@bot.message_handler(commands=['need'])
def send_welcome(message):
    """ Покажет какие ингредиенты нужно взять с собой """
    bot.reply_to(
        message,
        "Ждите..."
    )
    bot.reply_to(
        message,
        telemetron.how_ingredients_must_have()
    )


# Handle '/capacity'
@bot.message_handler(commands=['capacity'])
def send_capacity(message):
    """ Покажет текущую загрузку по всем автоматам """
    bot.reply_to(
        message,
        "Ждите..."
    )
    bot.reply_to(
        message,
        telemetron.show_ingredients()
    )


def get_configured_bot():
    return bot
