import os
from enum import Enum
from typing import List

import requests
from model import Stocks
from datetime import date, timedelta, datetime
from database import Dao
from customized_logger import get_logger

logger = get_logger("get_raw_data")


class RawDataKeys(Enum):
    TIME_SERIES = "Time Series (Daily)"
    OPEN_PRICE = "1. open"
    CLOSE_PRICE = "4. close"
    VOLUME = "6. volume"
    META_DATA = "Meta Data"
    LAST_REFRESHED = "3. Last Refreshed"
    DATE_FORMAT = "%Y-%m-%d"


def fetch_raw_stock_data(symbol: str, days_from_last: int = 14) -> List[Stocks]:
    """
    Fetch raw stock data from alpha vantage site, convert and return the list of Stocks.
    The range is `days_from_today`, including today. Default range is 2 weeks.

    :param symbol: The symbol of stock.
    :param days_from_last: specify the date range to be fetched. Default is 14 days from today inclusive.
    :return: a list of Stocks object.
    """

    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not alpha_vantage_api_key:
        logger.error("ALPHA_VANTAGE_API_KEY is not found in environment variable. Please setup the api key. Quit.")
        return

    # fetch data from alpha vantage
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={alpha_vantage_api_key}"
    r = requests.get(url)
    data = r.json()
    logger.info(f"Successfully fetched data of stock: {symbol}")

    # find the last refreshed date from meta data as the start_date.
    start_date = data[RawDataKeys.META_DATA.value][RawDataKeys.LAST_REFRESHED.value]
    start_date = datetime.strptime(start_date, RawDataKeys.DATE_FORMAT.value).date()
    data = data[RawDataKeys.TIME_SERIES.value]

    result = []
    # find most recent {days_from_last} data in the time series and add to result list.
    for i in range(days_from_last):
        target = (start_date - timedelta(days=i)).strftime(RawDataKeys.DATE_FORMAT.value)
        if target in data:
            stock = Stocks(symbol=symbol,
                           date=start_date - timedelta(days=i),
                           open_price=data[target][RawDataKeys.OPEN_PRICE.value],
                           close_price=data[target][RawDataKeys.CLOSE_PRICE.value],
                           volume=data[target][RawDataKeys.VOLUME.value]
                           )
            result.append(stock)

    return result


def main():
    target_stocks = ["IBM", "AAPL"]
    for stock in target_stocks:
        stocks = fetch_raw_stock_data(stock)
        Dao.upsert_stocks(stocks)


main()
