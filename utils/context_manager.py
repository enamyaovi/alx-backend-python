"""
Custom class-based context manager for handling MySQL database connections.
Establishes and tears down the connection cleanly with commit/rollback logic.
Uses seed-level exception handling for resilient runtime behavior.

Author: Cephas Tay
"""

import mysql
import mysql.connector
from typing import Optional, Any
from utils import seed

# pull configuration from env file for use throughout
get_config: dict = seed.get_config_parameters('db_secrets.env')

class DatabaseConnection:
    """
    Context manager for managing MySQL DB connections.

    Automatically handles opening and closing DB connections,
    as well as commits and rollbacks depending on success or error.
    Decorated with a custom exception handler for cleaner fail states.

    Args:
        config (dict): Configuration dictionary for DB connection params.
        db_name (str, optional): Override the DB name if provided.

    Raises:
        ValueError: If no database name is found in config or passed.
    """
    def __init__(self, config: dict = get_config, db_name: Optional[str] = None):
        if not db_name:
            if not config.get('database'):
                raise ValueError("No database provided to connect to")
        else:
            config['database'] = db_name
        
        self.config: dict = config
        self.connection: Optional[mysql.connector.connection_cext.CMySQLConnection] = None

    @seed.exception_handler
    def __enter__(self):
        """
        Establishes the database connection.

        Returns:
            connection (CMySQLConnection): Active MySQL connection object.
        """
        self.connection = mysql.connector.connect(**self.config) #type:ignore
        return self.connection

    @seed.exception_handler
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
        """
        Handles cleanup. Commits if all went well; rolls back otherwise.

        Args:
            exc_type (type): Exception type raised in the block.
            exc_value (Exception): Exception instance.
            traceback (traceback): Traceback object.

        Returns:
            bool: False to propagate exceptions, True to suppress.
        """
        if exc_type is None:
            self.connection.commit()  # type: ignore
        else:
            self.connection.rollback()  # type: ignore
        self.connection.close()  # type: ignore
        return False

def main():
    """
    Demo function to test connection and query.

    Executes a simple query to fetch the first 5 users.

    Returns:
        list: List of user records from the DB.
    """
    with DatabaseConnection(db_name='alx_prodev') as cnx:
        cursor = cnx.cursor() #type: ignore
        cursor.execute("SELECT * FROM users LIMIT 5")
        return cursor.fetchall()

if __name__ == "__main__":
    data = main()
    for user in data: #type: ignore
        print(user)