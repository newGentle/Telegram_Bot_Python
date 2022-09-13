import json
import requests
import telebot


class APIException(Exception):
    pass


TOKEN = '5627423398:AAHyMncrkbTHgxd1tpok0eT9zFi9INLzIS8'
APIKey = '013fade4a9fc0df00eb5c77266f991bd3836ecc36b8d5895ba1fced843fc6a0a'
bot = telebot.TeleBot(TOKEN)
currencies = {'доллар': 'USD',
              'фунт': 'GBP',
              'евро': 'EUR',
              'рубль': 'RUB',
              'биткоин': 'BTC',
              'эфириум': 'ETC'}


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
    if len(splitted) == 3 and splitted[-1].isdigit():
        _to, _from, _amount = splitted
        if _to not in list(currencies.keys()) and _from not in list(currencies.keys()):
            bot.send_message(message.chat.id, 'Недоступные валюты введены')
        elif _from == _to:
            bot.send_message(message.chat.id, 'Нельзя конвертировать одинаковые валюты')
        else:
            url = f'https://min-api.cryptocompare.com/data/price?fsym={currencies[_from]}&tsyms={currencies[_to]}'
            response = requests.get(url)
            result = json.loads(response.content)

            bot.reply_to(message, f'{_amount} {_from} = {result[currencies[_to]]} {_to}')
    else:
        bot.send_message(message.chat.id, 'неправильно введен запрос')



bot.polling(none_stop=True)
