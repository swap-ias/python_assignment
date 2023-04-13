from typing import List

import sqlalchemy
from sqlalchemy.orm import sessionmaker, session
from settings import get_settings
from model import Stocks

setting = get_settings()


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
    def insert_example(stocks: List[Stocks]) -> bool:
        try:
            _session = DB.session()
            _session.add(stocks)
            _session.commit()
            return True
        except:
            _session.rollback()
            return False
        finally:
            _session.close()
