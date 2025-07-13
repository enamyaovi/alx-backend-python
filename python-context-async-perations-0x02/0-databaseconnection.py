"""
Context manager for opening and closing MySQL database connections.
Makes use of a helper from `utils.seed` to load DB config and handle exceptions.
"""

import mysql
import mysql.connector
from utils import seed

# Load database config from .env file using the helper
get_config = seed.get_config_parameters('db_secrets.env')

class DatabaseConnection:
    """
    Class-based context manager for managing MySQL database connections.

    - Uses config from a secrets file (or accepts a custom config dict).
    - Allows optional override of the database name.
    - Automatically commits if no exception occurs, or rolls back if it does.
    - Exceptions in __enter__ and __exit__ are handled using a decorator.
    """

    def __init__(self, config: dict = get_config, db_name=None):
        if not db_name:
            if not config['database']:
                raise ValueError("No database provided to connect to")
        else:
            config['database'] = db_name
        
        self.config = config
        self.connection = None

    @seed.exception_handler
    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        return self.connection

    @seed.exception_handler
    def __exit__(self, type, value, traceback):
        if type is None:
            self.connection.commit()  # type: ignore
        else:
            self.connection.rollback()  # type: ignore
        self.connection.close()  # type: ignore
        return False

def main():
    # Basic usage of the context manager — select 5 users
    with DatabaseConnection(db_name='alx_prodev') as cnx:
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM users LIMIT 5")
        return cursor.fetchall()

if __name__ == "__main__":
    data = main()
    for user in data:
        print(user)
