import sqlite3
import functools
import inspect
import logging

# Set up error logger
error_logger = logging.getLogger("db_errors")
handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
formatter = logging.Formatter(fmt="{asctime} - {levelname}: {message}", style="{")
handler.setFormatter(formatter)
error_logger.addHandler(handler)
error_logger.setLevel(logging.ERROR)

def with_db_connection(func):
    """
    A decorator that injects a SQLite database connection into the wrapped function
    if one is not passed. It checks argument types and logs any errors.

    Automatically closes connections that it opens.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        conn = None
        should_close = False

        try:
            for name, value in bound.arguments.items():
                if name == 'conn' and not isinstance(value, sqlite3.Connection):
                    raise TypeError(f"Expected sqlite3.Connection for 'conn', got {type(value)}")
                if name == 'user_id' and not isinstance(value, int):
                    raise TypeError(f"Expected int for 'user_id', got {type(value)}")

            if 'conn' not in bound.arguments:
                conn = sqlite3.connect('users.db')
                should_close = True
                result = func(conn, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            return result

        except Exception as err:
            error_logger.exception(f"Error in {func.__name__}: {err}")
        finally:
            if should_close and conn:
                conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user by ID from the users table using the provided SQLite connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    user_id = 1
    user = get_user_by_id(user_id=user_id) #type:ignore

    if user:
        print(f"User found: {user}")
    else:
        print(f"No user found with ID {user_id}")