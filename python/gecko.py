import pandas as pd
import requests

from json import dump, load
from random import shuffle
from pprint import pprint
from sheet_updater import update_sheet
from datetime import datetime

TOKEN_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"

LIST_COINS_URL = "https://api.coingecko.com/api/v3/coins/list"


def query_coins() -> list[str]:
    coins = requests.get(LIST_COINS_URL).json()
    coins = [coin['name'] for coin in coins]
    return coins


def read_coins() -> list[str]:
    with open('coins.json') as f:
        return load(f)


def get_prices(coin_param: str):
    # print(TOKEN_PRICE_URL.format(coin_param))
    # return
    resp = requests.get(TOKEN_PRICE_URL.format(coin_param))
    resp.raise_for_status()
    print(resp)
    return resp.json()


def parser_prices(api_price_response: dict):
    rows = []
    last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for k, v in api_price_response.items():
        if k not in ['404']:
            if 'usd' not in v:
                continue
            rows.append([k, v['usd'], last_updated])
    return pd.DataFrame(rows, columns=['token', 'price (usd)', 'last update'])


if __name__ == '__main__':
    coins = read_coins()
    shuffle(coins)
    prices = get_prices(','.join(coins[:200]))
    pprint(prices)
    table = parser_prices(prices)
    update_sheet('test sheet', table)