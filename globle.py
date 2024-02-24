import logging
from configparser import ConfigParser
from clickhouse_orm import Database
from clickhouse_orm import Database
from fastapi import FastAPI

LOGGER = logging.getLogger()
logging.basicConfig(level="DEBUG")
app = FastAPI()
config = ConfigParser()

pdf_max_pages = 20


def init_database():
    config.read('config.ini')
    sections = config.sections()
    if len(sections) < 1:
        return None
    if ((config.get("DefaultDatabase", "db_name") == "") or
            (config.get("DefaultDatabase", "db_url") == "")):
        return None
    pdf_max_pages = config.getint("System", "pdf_max_pages")
    db = Database(db_name=config.get("DefaultDatabase", "db_name"),
                  db_url=config.get("DefaultDatabase", "db_url"),
                  username=config.get("DefaultDatabase", "username"),
                  password=config.get("DefaultDatabase", "password"), timeout=100)
    if not db.db_exists:
        return None

    return db


db = init_database()
