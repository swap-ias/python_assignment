import os
from typing import List

import requests
from model import Stocks
from datetime import date, timedelta
from database import Dao
from customized_logger import get_logger

logger = get_logger("get_raw_data")


def fetch_raw_stock_data(symbol: str, days_from_today: int = 14) -> List[Stocks]:
    """
    Fetch raw stock data from alpha vantage site, convert and return the list of Stocks.
    The range is `days_from_today`, including today. Default range is 2 weeks.

    :param symbol: The symbol of stock.
    :param days_from_today: specify the date range to be fetched. Default is 14 days from today inclusive.
    :return: a list of Stocks object.
    """

    alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not alpha_vantage_api_key:
        logger.error("ALPHA_VANTAGE_API_KEY is not found in environment variable. Please setup the api key. Quit.")
        return

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={alpha_vantage_api_key}"
    r = requests.get(url)
    data = r.json()
    data = data['Time Series (Daily)']
    logger.info(f"Successfully fetched data of stock: {symbol}")

    today = date.today()
    result = []
    for i in range(days_from_today):
        target = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        if target in data:
            result.append(_convert_raw_to_stock(symbol, today - timedelta(days=i), data[target]))

    return result


def _convert_raw_to_stock(symbol, day, raw_data):
    open_price_key = "1. open"
    close_price_key = "4. close"
    volume_key = "6. volume"
    return Stocks(symbol=symbol,
                  date=day,
                  open_price=raw_data[open_price_key],
                  close_price=raw_data[close_price_key],
                  volume=raw_data[volume_key]
                  )


def main():
    target_stocks = ["IBM", "AAPL"]
    for stock in target_stocks:
        stocks = fetch_raw_stock_data(stock)
        Dao.upsert_stocks(stocks)


main()
