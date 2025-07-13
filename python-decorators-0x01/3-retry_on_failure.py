import time
import sqlite3
import functools

# Import connection decorator and logger
with_db_connection_module = __import__('1-with_db_connection')
with_db_connection = with_db_connection_module.with_db_connection
error_logger = with_db_connection_module.error_logger

def retry_on_failure(retries=2, delay=1):
    """
    A decorator that retries a function if it fails with a sqlite3-related error.
    Retries happen up to the number specified, with a pause between each attempt.
    Other exceptions are not retried and will raise immediately.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.Error as err:
                error_logger.error(f"Initial call failed with sqlite3 error: {err}")

                for count in range(retries):
                    error_logger.info(f"Retrying {count + 1} of {retries} after {delay} second(s)")
                    time.sleep(delay)
                    try:
                        return func(*args, **kwargs)
                    except sqlite3.Error as e:
                        error_logger.error(f"Retry {count + 1} failed: {e}")

                error_logger.critical(f"All {retries} retry attempts failed for {func.__name__}")
                return None, retries
            except Exception as other:
                error_logger.exception(f"Non-sqlite3 error occurred: {other}")
                raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Tries to fetch all users from the users table.
    Will retry only if a sqlite3.Error is raised.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()


# Run with retry logic
if __name__ == "__main__":
    users, retries = fetch_users_with_retry()
    if users:
        print(users)
    else:
        print(f"Failed to fetch users after {retries} retry attempts.")
