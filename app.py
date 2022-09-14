import telebot
from config import TOKEN, currencies
from extensions import APIException, Convert

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', ])
def handler_start_help(message):
    bot.send_message(message.chat.id, '''
Бот конвертирует доступные валюты
в формате - доллар евро 1
имеется ввиду курс 1-евро в долларах.
Все валюты можно посмотреть по команде /values''')


@bot.message_handler(commands=['values', ])
def handler_values(message):
    curr = 'Доступные валюты:\n'
    list_keys = list(currencies.keys())
    for keys in list_keys:
        curr += f'{keys}\n'
    bot.send_message(message.chat.id, curr)


@bot.message_handler(content_types=['text', ])
def handler_text(message):
    splitted = message.text.lower().split()
    try:
        converted = Convert.convert(splitted)
        bot.send_message(message.chat.id, converted)
    except APIException as e:
        bot.send_message(message.chat.id, str(e))

        
bot.polling(none_stop=True)
