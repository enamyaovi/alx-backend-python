
import time
import sqlite3 
import functools

with_db_connection = __import__('1-with_db_connection').with_db_connection

#### paste your with_db_decorator here
def retry_on_failure(retries=None, delay=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                # investigate why a while loop doesn't run
                # while retries > 0:
                    # time.sleep(delay)
                    # print(f"slept trying func call, retries{retries}")
                    # retries -= 1
                    # func(*args, **kwargs)
                for count in range(retries):
                    print(f"Retring to execute {count + 1} times")
                    time.sleep(delay)
                    print(f"slept for {delay} seconds")
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"{e}")       
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

""" your code goes here"""

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)