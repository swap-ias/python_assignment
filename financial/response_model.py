from typing import List, Optional
from pydantic import BaseModel
from model import Stocks
from settings import get_settings
from decimal import Decimal


class StockModel(BaseModel):
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str


class Pagination(BaseModel):
    count: int
    page: int
    limit: int
    pages: int


class ErrorInfo(BaseModel):
    error: str = ""


class FinancialDataResponse(BaseModel):
    data: List[Optional[StockModel]]
    pagination: Optional[Pagination]
    info: ErrorInfo


def convert_stocks_to_stocks_model(stocks: List[Stocks]):
    data = []
    for stock in stocks:
        s = stock.to_dict()
        model = StockModel(symbol=s['symbol'],
                           date=s['date'].strftime(get_settings().date_format),
                           open_price=str(s['open_price']),
                           close_price=str(s['close_price']),
                           volume=s['volume']
                           )
        data.append(model)
    return data


class StatisticStock(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    average_daily_open_price: Decimal
    average_daily_close_price: Decimal
    average_daily_volume: int


class StatisticDataResponse(BaseModel):
    data: Optional[StatisticStock]
    info: ErrorInfo

