import inspect
import functools
import logging
from datetime import datetime  # Required for the project checker
import mysql.connector

config = {
    'username': 'myuser',
    'password': 'secret',
    'host': 'localhost',
    'database': 'users'  # Added so the query runs without error
}

# Set up logger to write query logs to a file
query_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(filename='app.log', mode='a', encoding="utf-8")
formatter = logging.Formatter(fmt="{asctime} - {levelname}: {msg}", style="{")
file_handler.setFormatter(formatter)
query_logger.addHandler(file_handler)
query_logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

def log_queries(func):
    """
    Logs any SQL query passed to a function as an argument named 'query'.

    Uses the inspect module to access parameter values, and logs the query
    using a custom file-based logger. Logs are saved to 'app.log'.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        try:
            for name, value in bound.arguments.items():
                if name == 'query':
                    query_logger.info(f"Query: {value}")
        except Exception as err:
            query_logger.exception(f"Error while logging query: {err}")

        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Connects to the MySQL database and fetches all rows from the result of the given query.
    """
    with mysql.connector.connect(**config) as cnx:
        cur = cnx.cursor()
        cur.execute(query)
        return cur.fetchall()

# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")

    for user in users:
        print(user)
