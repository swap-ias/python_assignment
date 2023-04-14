import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings

DEFAULT_DB = {
    "user": os.getenv("DB_USER", "financial_user"),
    "password": os.getenv("DB_PASSWORD", "financial_pass"),
    "host": os.getenv("DB_HOST", "mysql"),
    "db": os.getenv("DB_NAME", "financial_db"),
    "port": os.getenv("DB_PORT", "3306"),
}

load_dotenv()


def generate_db_uri(protocol, user, password, host, db, port):
    return f"{protocol}://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"


class Settings(BaseSettings):
    database_uri: str = generate_db_uri("mysql+pymysql", **DEFAULT_DB)
    date_format: str = "%Y-%m-%d"


@lru_cache()
def get_settings():
    # get current environment
    env = os.getenv("ENV", "local")

    if env == "local":
        return Settings()



