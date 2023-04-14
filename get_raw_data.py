from model import Stocks
from datetime import date, timedelta
from database import Dao
from customized_logger import get_logger

logger = get_logger("get_raw_data")

stocks = []
today = date.today()
for i in range(2001):
    stock = Stocks(symbol="IBM", date=today+timedelta(days=i), open_price=i+0.98, close_price=i+0.23, volume=i*100)
    stocks.append(stock)


# Dao.insert_stocks(stocks)
Dao.upsert_stocks(stocks)
