from time import sleep

import pandas as pd
import requests

from datetime import datetime
from json import load
from pprint import pprint
from sheet_updater import update_sheet

MAX_PAGE_SIZE = 250

TOKEN_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"

LIST_COINS_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={}&page={}&sparkline=false' "


def query_coins() -> list[dict]:
    coins = []
    for page in range(1, 5):
        print(f'querying page #: {page} of size: {MAX_PAGE_SIZE}')
        coins += requests.get(LIST_COINS_URL.format(MAX_PAGE_SIZE, page)).json()
    return coins


def read_coins() -> list[dict]:
    with open('coins.json') as f:
        return load(f)


def get_prices(coin_param: str):
    resp = requests.get(TOKEN_PRICE_URL.format(coin_param))
    resp.raise_for_status()
    print(resp)
    return resp.json()


def parser_prices(api_market_response: list[dict]) -> pd.DataFrame:
    rows = []
    last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    columns = {'name', 'market_cap', 'current_price', 'market_cap_change_percentage_24h', 'fully_diluted_valuation'}
    for coin_data in api_market_response:
        row = dict()
        for k, v in coin_data.items():
            if k not in columns:
                continue
            if v in [None]:
                continue
            row[k.replace('_', ' ')] = v
        row['last updated'] = last_updated
        rows.append(row)
    return pd.DataFrame(rows).fillna('')


def main():
    coins = query_coins()  # read_coins()
    pprint(coins)
    table = parser_prices(coins)
    print(table)
    sheet_title = 'gecko'
    print(f"Updating spreadsheet: '{sheet_title}'...")
    update_sheet(sheet_title, table)
    print("DONE")


if __name__ == '__main__':
    while True:
        main()
        print("sleeping...")
        sleep(3600)