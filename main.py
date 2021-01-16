import os
from decimal import Decimal

import tinvest
from dotenv import load_dotenv
from pycbrf import ExchangeRates

from pytz import timezone
from datetime import datetime

load_dotenv()

def localize(d: datetime) -> datetime:
    return timezone('Europe/Moscow').localize(d)

def get_now() -> datetime:
    return localize(datetime.now())

def get_usd_course() -> Decimal:
    rates = ExchangeRates(get_now())
    return rates['USD'].value

if __name__ == '__main__':

    TOKEN = os.getenv('TOKEN')

    client = tinvest.SyncClient(TOKEN)

    response = client.get_portfolio()
    positions = response.payload.positions

    csv_rows = []
    csv_rows.append(','.join(['name',
                              'average_position_price',
                              'currency',
                              'balance',
                              'expected_yield',
                              'ticker']))

    for position in positions:
        csv_rows.append(','.join(map(str, [position.name,
                                           position.average_position_price.value,
                                           position.average_position_price.currency.value,
                                           position.balance,
                                           position.expected_yield.value,
                                           position.ticker])))
    with open('positions.csv', 'w') as f:
        f.write('\n'.join(csv_rows))
