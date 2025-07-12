import time
import sqlite3 
import functools
import inspect

# Import decorator that provides a database connection
with_db_connection = __import__('1-with_db_connection').with_db_connection

# Global dictionary to cache query results
query_cache = {}

# Decorator to cache results of SQL queries
def cache_query(func, counter_dict={}):
    counter_dict[func] = 0
    counter_dict['last_query'] = None

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Bind arguments to their parameter names
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        counter_dict[func] += 1

        # Extract current SQL query from arguments
        current_query = None
        for name, value in bound.arguments.items():
            if name == 'query':
                current_query = str(value)

        # If the query is new, evaluate and cache it
        if counter_dict['last_query'] != current_query:
            print('New query detected')
            counter_dict['last_query'] = current_query
            try:
                # If already in cache, return it
                if current_query in query_cache:
                    return query_cache[current_query]

                # Otherwise, execute and cache the result
                result = func(*args, **kwargs)
                if result:
                    query_cache[current_query] = result
                    return query_cache[current_query]
            except Exception as e:
                print(f"[ERROR]: {e}")
        else:
            # Query is unchanged, return cached result
            print(f"Old query: returning cached result for query: {current_query}")
            return query_cache[current_query]

    return wrapper

# Function to fetch users using the cache_query decorator
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Test calls
users = fetch_users_with_cache(query="select * from users;")
users_again = fetch_users_with_cache(query="select * from users;")
users_again = fetch_users_with_cache(query="select * from users;")
users_again = fetch_users_with_cache(query="select * from users where id = 3;")
users_again = fetch_users_with_cache(query="select * from users where id = 3;")
users_again = fetch_users_with_cache(query="select * from users where id = 1;")
