from typing import List
import sqlalchemy
from sqlalchemy.orm import sessionmaker, session
from settings import get_settings
from model import Stocks
from customized_logger import get_logger

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
    def insert_stocks(stocks: List[Stocks], batch_size: int = 1000):
        """
        Insert stock data with batches. Default batch size is 1000.
        If exception happened during the process, the whole data will be rolled back.

        :param stocks:  List of Stocks object.
        :param batch_size:  The size of batch insert.
        :return:
        """

        _session = DB.session()
        try:
            left, right = 0, batch_size
            while left < len(stocks):
                _session.bulk_save_objects(stocks[left:right])
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
