import sys
from configparser import ConfigParser

from clickhouse_orm import Database


def _get_db(db_name):
    """
    Returns a Database instance using connection information
    from the command line arguments (optional).
    """
    db_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8123/"
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    return Database(db_name, db_url, username, password, readonly=True)

