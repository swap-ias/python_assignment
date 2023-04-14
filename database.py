from decimal import Decimal
from typing import List, Optional, Tuple
import sqlalchemy
from sqlalchemy.orm import sessionmaker, session

from errors import DatabaseValueError
from settings import get_settings
from model import Stocks
from datetime import date
from customized_logger import get_logger
from sqlalchemy.dialects.mysql import insert as mysql_upsert

setting = get_settings()
logger = get_logger("database")


class DB:
    engine_cache = None

    @staticmethod
    def engine():
        if DB.engine_cache is None:
            DB.engine_cache = sqlalchemy.create_engine(setting.database_uri, echo=False, echo_pool=False)
        return DB.engine_cache

    @staticmethod
    def session() -> session:
        Session = sessionmaker()
        engine = DB.engine()
        Session.configure(bind=engine)
        return Session()


class Dao:

    @staticmethod
    def upsert_stocks(stocks: List[Stocks], batch_size: int = 1000):
        """
        Upsert stock data with batches. Default batch size is 1000.
        If duplicates is found for (symbol, date) unique key, the (open_price, close_price, volume) will be updated.
        If exception happened during the process, the whole data will be rolled back.

        :param stocks:  List of Stocks object.
        :param batch_size:  The size of batch insert.
        """
        sess = DB.session()
        rows = [stock.to_dict() for stock in stocks]
        try:
            left, right = 0, batch_size
            while left < len(rows):
                stmt = mysql_upsert(Stocks).values(rows[left: right])
                stmt = stmt.on_duplicate_key_update({"open_price": stmt.inserted.open_price,
                                                     "close_price": stmt.inserted.close_price,
                                                     "volume": stmt.inserted.volume})
                sess.execute(stmt)

                left = right
                right += batch_size
            sess.commit()
            logger.info(f"Inserted {len(stocks)} stock items.")
        except Exception as e:
            logger.error("Error happened while inserting stock items. Trying rollback database.")
            sess.rollback()
            raise e
        finally:
            sess.close()

    @staticmethod
    def query_stocks(symbol: Optional[str], start_date: Optional[date], end_date: Optional[date], page_size: int, page: int) -> Tuple[int, List[Stocks]]:
        """
        Return the total count of stocks and a list of Stocks object based on the parameters.

        Warn: this method is using offset and limit to get the page of data, it could be slow when the
        page is becoming bigger for large datasets.

        :param symbol: the symbol of stock
        :param start_date: the start range of date to be returned. If it is None, start_date will be the earliest date.
        :param end_date: the end range of date to be returned. If it is None, end_date will be the latest date.
        :param page_size: the size of data to be returned in one page.
        :param page: the page number, start from 1.
        :return: a Tuple of (total_count, page_of_stocks_data)
        """

        sess = DB.session()

        try:
            query = sess.query(Stocks)
            count_query = sess.query(sqlalchemy.func.count("*")).select_from(Stocks)
            if symbol:
                query = query.filter(Stocks.symbol == symbol)
                count_query = count_query.filter(Stocks.symbol == symbol)
            if start_date:
                query = query.filter(Stocks.date >= start_date)
                count_query = count_query.filter(Stocks.date >= start_date)
            if end_date:
                query = query.filter(Stocks.date <= end_date)
                count_query = count_query.filter(Stocks.date <= end_date)

            query = query.offset((page-1) * page_size).limit(page_size)
            stock_data = query.all()
            count = count_query.scalar()

            if not count:
                raise DatabaseValueError(f"Could not find result. Please check the inputs.")

            return count, stock_data
        except Exception as e:
            logger.error("Error happened while query stock items.")
            raise e
        finally:
            sess.close()

    @staticmethod
    def avg_stock(symbol: str, start_date: date, end_date: date):
        sess = DB.session()
        try:
            query = sess.query(sqlalchemy.func.avg(Stocks.open_price),
                               sqlalchemy.func.avg(Stocks.close_price),
                               sqlalchemy.func.avg(Stocks.volume))\
                .filter(Stocks.symbol == symbol)\
                .filter(Stocks.date >= start_date)\
                .filter(Stocks.date <= end_date)

            avg_open_price, avg_close_price, avg_volume = query.one_or_none()
            if not avg_open_price or not avg_close_price or not avg_volume:
                raise DatabaseValueError(f"Could not find result. Please check the inputs.")

            return avg_open_price.quantize(Decimal('.01')), avg_close_price.quantize(Decimal('.01')), avg_volume.quantize(Decimal('.01'))
        except Exception as e:
            logger.error("Error happened while query statistic data.")
            raise e
        finally:
            sess.close()

