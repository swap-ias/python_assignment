from typing import Optional
from fastapi import APIRouter, Query
from customized_logger import get_logger
from errors import DatabaseValueError
from .response_model import FinancialDataResponse, Pagination, ErrorInfo, convert_stocks_to_stocks_model, StatisticStock, StatisticDataResponse
from settings import get_settings
from datetime import datetime
from database import Dao
import math

financial_router = APIRouter()
logger = get_logger("financial_api")
setting = get_settings()


@financial_router.get("/financial_data",
                      response_model=FinancialDataResponse)
def financial_data(start_date: Optional[str] = Query(default=None, min_length=10, max_length=10,
                                                     regex="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
                   end_date: Optional[str] = Query(default=None, min_length=10, max_length=10,
                                                   regex="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
                   symbol: Optional[str] = Query(default=None, min_length=1, regex="^[a-zA-Z_.]+$"),
                   limit: int = Query(default=5, ge=1, le=100),
                   page: int = Query(default=1, ge=1)
                   ):
    logger.info(
        f"requested api/financial_data, start_date: {start_date}, end_date: {end_date}, symbol: {symbol}, limit: {limit}, page: {page}.")

    try:
        if start_date:
            start_date = datetime.strptime(start_date, setting.date_format).date()
        if end_date:
            end_date = datetime.strptime(end_date, setting.date_format).date()

        if start_date and end_date and start_date > end_date:
            return FinancialDataResponse(data=[], page=Pagination(page=page, limit=limit), info=ErrorInfo(
                error=f"start_date={start_date} is bigger than end_date={end_date}."))

        count, stocks = Dao.query_stocks(symbol, start_date, end_date, limit, page)

        return FinancialDataResponse(data=convert_stocks_to_stocks_model(stocks),
                                     pagination=Pagination(count=count, page=page, limit=limit,
                                                           pages=math.ceil(count / limit)),
                                     info=ErrorInfo())
    except ValueError as e1:
        return FinancialDataResponse(data=[], page=Pagination(page=page, limit=limit), info=ErrorInfo(
            error=f"Value error for start_date={start_date} or end_date={end_date}."))
    except DatabaseValueError as e2:
        return StatisticDataResponse(data=None, info=ErrorInfo(
            error=str(e2)))
    except Exception as e:
        return FinancialDataResponse(data=[], page=Pagination(page=page, limit=limit), info=ErrorInfo(
            error="Error happened while query data."))


@financial_router.get("/statistics")
def statistics(start_date: str = Query(min_length=10, max_length=10,
                                       regex="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
               end_date: str = Query(min_length=10, max_length=10,
                                     regex="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
               symbol: str = Query(min_length=1, regex="^[a-zA-Z_.]+$")
               ):
    logger.info(
        f"requested api/statistics, start_date: {start_date}, end_date: {end_date}, symbol: {symbol}.")
    try:
        start_date = datetime.strptime(start_date, setting.date_format).date()
        end_date = datetime.strptime(end_date, setting.date_format).date()
        if start_date > end_date:
            return StatisticDataResponse(data=None, info=ErrorInfo(
                error=f"start_date={start_date} is bigger than end_date={end_date}."))

        avg_open_price, avg_close_price, avg_volume = Dao.avg_stock(symbol, start_date, end_date)
        data = StatisticStock(symbol=symbol,
                              start_date={start_date},
                              end_date={end_date},
                              average_daily_open_price=avg_open_price,
                              average_daily_close_price=avg_close_price,
                              average_daily_volume=avg_volume)
        return StatisticDataResponse(data=data, info=ErrorInfo())
    except ValueError as e1:
        return StatisticDataResponse(data=None, info=ErrorInfo(
            error=f"value error for start_date={start_date} or end_date={end_date}."))
    except DatabaseValueError as e2:
        return StatisticDataResponse(data=None, info=ErrorInfo(
            error=str(e2)))
    except Exception as e:
        return StatisticDataResponse(data=None, info=ErrorInfo(
            error=f"Error happened when query statistic data."))

