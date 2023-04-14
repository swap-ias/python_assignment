from sqlalchemy import VARCHAR, Column, DATE, DECIMAL, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Stocks(Base):
    __tablename__ = 'financial_data'
    __table_args__ = (UniqueConstraint('symbol', 'date', name='_symbol_date_unique'),
                      {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_bin"}
                      )
    id = Column("id", BIGINT, primary_key=True, autoincrement=True)
    symbol = Column("symbol", VARCHAR(32), nullable=False, unique=False, index=True)
    date = Column("date", DATE, nullable=False, unique=False, index=True)
    open_price = Column("open_price", DECIMAL(19, 2), nullable=False, unique=False, index=False)
    close_price = Column("close_price", DECIMAL(19, 2), nullable=False, unique=False, index=False)
    volume = Column("volume", BIGINT, nullable=False, unique=False, index=False)

    def __repr__(self):
        return f'Stocks(id:{self.id}, symbol:{self.symbol}, date:{self.date}, open_price:{self.open_price}, close_price:{self.close_price}, volume:{self.volume})'

    def to_dict(self):
        return {"symbol": self.symbol,
                "date": self.date,
                "open_price": self.open_price,
                "close_price": self.close_price,
                "volume": self.volume}
