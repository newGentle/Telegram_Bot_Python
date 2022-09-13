import json

import requests
import telebot

TOKEN = '5627423398:AAFtKXYTQhLYYM6eb31N4mrjAUompRdBbDU'

bot = telebot.TeleBot(TOKEN)
currencies = {'доллар': 'USD',
              'фунт': 'GBP',
              'евро': 'EUR',
              'рубль': 'Ruble'}


@bot.message_handler(commands=['start', 'help', ])
def handler_start_help(message):
    bot.reply_to(message, 'Welcome to Currency Converter !!!')
    bot.send_message(message.chat.id, f'Hi {message.chat.username}')


@bot.message_handler(commands=['values'], )
def handler_values(message):
    curr = ''
    for j in currencies:
        curr += f'{currencies[j]}\n'
    bot.send_message(message.chat.id, curr)

@bot.message_handler(content_types=['text',])
def handler_text(message):
    payload = {}
    API_TOKEN = {'apikey': 'A3hZn9HxG9nJIL89MgHJuJjQnpsnwOjQ'}
    _to, _from, _amount = message.text.split()
    
    url = f"https://api.apilayer.com/fixer/convert?to={currencies[_from]}&from={currencies[_to]}&amount={_amount}"

    # response = requests.request("GET", url, headers=API_TOKEN, data=payload)
    response = requests.get(url, headers=API_TOKEN)
    # status_code = response.status_code
    # result = response.content
    # print(result)
    response = json.loads(response.content)
    bot.reply_to(message, f'{_amount} {_to} в {_from} = {response["result"]}')
bot.polling(none_stop=True)
