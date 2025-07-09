
import time
import sqlite3 
import functools, inspect

with_db_connection = __import__('1-with_db_connection').with_db_connection


query_cache = {}
x = 1
"""your code goes here"""
# first_query = None
# next_query = None

def cache_query(func, counter_dict={}):
    counter_dict[func] = 0
    counter_dict['last_query'] = None
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # inspect query from signature
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        counter_dict[func] += 1

        current_query = None
        for name, value in bound.arguments.items():
            if name == 'query':
                current_query = str(value)
        
                
        if counter_dict['last_query'] != current_query:
            print('New query detected')
            counter_dict['last_query'] = current_query
            try:
                    #now evaluate the function and update the query_cache
                if current_query in query_cache:
                    return query_cache[f'{current_query}']

                result = func(*args, **kwargs)
                query_cache.clear()
                if result:
                    for row in result:
                        query_cache[f'{current_query}'] = row
                    return query_cache[f'{current_query}']
            except Exception as e:#will work on later just checking
                print(f"{e}")
        else:
            print(f"old query: returning cached result for query: {current_query}")
            return query_cache[f'{current_query}']
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="select * from users;")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="select * from users;")
users_again = fetch_users_with_cache(query="select * from users;")
users_again = fetch_users_with_cache(query="select * from users where id = 3;")
users_again = fetch_users_with_cache(query="select * from users where id = 3;") #there will be a bug as it will be evaluated against the first query not dynamic enough to detect this is a query like before

users_again = fetch_users_with_cache(query="select * from users where id = 1;")
