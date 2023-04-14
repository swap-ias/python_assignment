from typing import List
import sqlalchemy
from sqlalchemy.orm import sessionmaker, session
from settings import get_settings
from model import Stocks
from customized_logger import get_logger
from sqlalchemy.dialects.mysql import insert as mysql_upsert

setting = get_settings()
logger = get_logger("database")


class DB:
    engine_cache = None

    @staticmethod
    def engine():
        if DB.engine_cache is None:
            DB.engine_cache = sqlalchemy.create_engine(setting.database_uri, echo=True, echo_pool=True)
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
        :return:
        """
        _session = DB.session()
        rows = [stock.to_dict() for stock in stocks]
        try:
            left, right = 0, batch_size
            while left < len(rows):
                stmt = mysql_upsert(Stocks).values(rows[left: right])
                stmt = stmt.on_duplicate_key_update({"open_price": stmt.inserted.open_price,
                                                     "close_price": stmt.inserted.close_price,
                                                     "volume": stmt.inserted.volume})
                _session.execute(stmt)

                left = right
                right += batch_size
            _session.commit()
            logger.info(f"Inserted {len(stocks)} stock items.")
        except Exception as e:
            logger.error("Error happened while inserting stock items. Trying rollback database.")
            _session.rollback()
            raise e
        finally:
            _session.close()
