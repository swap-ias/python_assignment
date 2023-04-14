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
    try:
        # convert start_date and end_date from string to date
        if start_date:
            start_date = datetime.strptime(start_date, setting.date_format).date()
        if end_date:
            end_date = datetime.strptime(end_date, setting.date_format).date()

        if start_date and end_date and start_date > end_date:
            return FinancialDataResponse(data=[], page=None, info=ErrorInfo(
                error=f"start_date={start_date} is bigger than end_date={end_date}."))

        # get total count of results, and a page of result from database
        count, stocks = Dao.query_stocks(symbol, start_date, end_date, limit, page)

        return FinancialDataResponse(data=convert_stocks_to_stocks_model(stocks),
                                     pagination=Pagination(count=count, page=page, limit=limit,
                                                           pages=math.ceil(count / limit)),
                                     info=ErrorInfo())
    except ValueError as e1:
        return FinancialDataResponse(data=[], page=None, info=ErrorInfo(
            error=f"Value error. Possibly start_date={start_date} or end_date={end_date} can't be converted to date."))
    except DatabaseValueError as e2:
        return FinancialDataResponse(data=[], page=None, info=ErrorInfo(
            error=str(e2)))
    except Exception as e:
        return FinancialDataResponse(data=[], page=None, info=ErrorInfo(
            error="Error happened while query data."))


@financial_router.get("/statistics")
def statistics(start_date: str = Query(min_length=10, max_length=10,
                                       regex="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
               end_date: str = Query(min_length=10, max_length=10,
                                     regex="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
               symbol: str = Query(min_length=1, regex="^[a-zA-Z_.]+$")
               ):
    try:
        # convert start_date and end_date from string to date
        start_date = datetime.strptime(start_date, setting.date_format).date()
        end_date = datetime.strptime(end_date, setting.date_format).date()
        if start_date > end_date:
            return StatisticDataResponse(data=None, info=ErrorInfo(
                error=f"start_date={start_date} is bigger than end_date={end_date}."))

        # get avg data from database
        avg_open_price, avg_close_price, avg_volume = Dao.avg_stock(symbol, start_date, end_date)

        # convert data to response model
        data = StatisticStock(symbol=symbol,
                              start_date=start_date.strftime(setting.date_format),
                              end_date=end_date.strftime(setting.date_format),
                              average_daily_open_price=avg_open_price,
                              average_daily_close_price=avg_close_price,
                              average_daily_volume=avg_volume)
        return StatisticDataResponse(data=data, info=ErrorInfo())
    except ValueError as e1:
        return StatisticDataResponse(data=None, info=ErrorInfo(
            error=f"Value error. Possibly start_date={start_date} or end_date={end_date} can't be converted to date."))
    except DatabaseValueError as e2:
        return StatisticDataResponse(data=None, info=ErrorInfo(
            error=str(e2)))
    except Exception as e:
        return StatisticDataResponse(data=None, info=ErrorInfo(
            error=f"Error happened when query statistic data."))

