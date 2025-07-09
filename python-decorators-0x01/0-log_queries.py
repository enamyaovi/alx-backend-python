import inspect, functools
import logging

query_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(filename='app.log',mode='a', encoding="utf-8")
formatter = logging.Formatter(style="{", fmt="{asctime} - {levelname}: {msg}")
file_handler.setFormatter(formatter)
query_logger.addHandler(file_handler)
query_logger.setLevel("INFO")
file_handler.setLevel("INFO")

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        sig = inspect.signature(func)

        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        try:
            for name, value in bound.arguments.items():
                if name == 'query':
                #do something like logging the query
                    print(value)
                    query_logger.info(msg={value})
        except Exception as err:
            query_logger.exception({err})

        return func(*args, **kwargs)
    return wrapper


# @log_queries
# def fetch_all_users(query):
    # conn = sqlite3.connect('users.db')
    # cursor = conn.cursor()
    # cursor.execute(query)
    # results = cursor.fetchall()
    # conn.close()
    # return results

@log_queries
def fetch_all_users(query):
    print('Perform Database Operations')

users = fetch_all_users(query="SELECT * FROM users")