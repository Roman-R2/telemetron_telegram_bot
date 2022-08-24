import os

import telebot
from dotenv import load_dotenv

from services.telemetron import TelemetronRequests
from settings import settings

#
#
# class TelegramBot:
#     def __init__(self, telegram_token, chat_id):
#         self.chat_id = chat_id
#         self.bot = telebot.TeleBot(telegram_token, threaded=False)
#
#     def send_message_to_channel(self, message: str):
#         self.bot.send_message(self.chat_id, message)
#         # self.bot.polling()
#
#
# class InitBot:
#
#     def __init__(self):
#         load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
#
#         self.telegram_token = os.getenv('TELEGRAM_TOKEN')
#         self.chat_id = os.getenv('CHAT_ID')
#
#     def __start(self):
#         random_cite = self.db_driver.get_random_cite()
#         cite_string = f""" {random_cite[2]}\n-----------------\n{random_cite[3]}"""
#
#         # print(random_cite, cite_string)
#
#         if cite_string:
#             TelegramBot(
#                 self.telegram_token,
#                 self.chat_id
#             ).send_message_to_channel(
#                 cite_string
#             )
#             print('Цитата отправлена...')
#         else:
#             print('Логируем ошибку...')
#
#     @staticmethod
#     def start():
#         return InitBot().__start()
#

# if __name__ == '__main__':
#     print(f'Это модуль {__name__}')

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


bot.infinity_polling()
