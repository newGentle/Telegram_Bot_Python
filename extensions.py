import json
import requests
from config import currencies, APIKey
import traceback


class APIException(Exception):
    pass


class Convert():
    @staticmethod
    def convert(splitted):
        if len(splitted) == 3 and splitted[-1].isdigit():
            _to, _from, _amount = splitted
            if _to not in list(currencies.keys()) or _from not in list(currencies.keys()):
                raise APIException('Введены недоступные валюты\nДоступные валюты /values')
            elif _from == _to:
                raise APIException(f'Нельзя конвертировать одинаковые валюты {_from} на {_to}')
            elif int(_amount) > 1:
                raise APIException('Нельзя получить курс больше единицы\nПодробно можно посмотреть /help')
            else:
                url = f'https://min-api.cryptocompare.com/data/price?fsym={currencies[_from]}&tsyms={currencies[_to]}{APIKey}'
                try:
                    response = requests.get(url)
                    result = json.loads(response.content)
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    raise APIException(f'Сервер временно не доступен\nПопробуйте снова чуть позже\nИзвините за неудобства')
                else:
                    return f'{_amount} {_from} = {result[currencies[_to]]} {_to}'
        else:
            raise APIException('неправильно введен запрос\nПодробно можно посмотреть /help')
            
