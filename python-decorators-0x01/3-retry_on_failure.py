import time
import sqlite3
import functools

with_db_connection = __import__('1-with_db_connection').with_db_connection

# Decorator to retry function execution on failure
def retry_on_failure(retries=None, delay=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                for count in range(retries):
                    print(f"Retrying to execute {count + 1} times")
                    time.sleep(delay)
                    print(f"Slept for {delay} seconds")
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"[ERROR]: {e}")
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
