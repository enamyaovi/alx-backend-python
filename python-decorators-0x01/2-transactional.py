import sqlite3 
import functools, inspect

with_db_connection = __import__('1-with_db_connection').with_db_connection

"""your code goes here"""
def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        try:
            func(*args, **kwargs)
            print("Called Transactional")

        except (sqlite3.Error, sqlite3.Warning, sqlite3.InterfaceError, sqlite3.DatabaseError, sqlite3.DataError, sqlite3.IntegrityError, sqlite3.InternalError, sqlite3.NotSupportedError, Exception):
            #get connection
            for name, value in bound.arguments.items():
                if name == 'conn':
                    conn = value
                    conn.rollback()
                    print("Changes Rolled back")
        else:
            #get connection
            for name, value in bound.arguments.items():
                if name == 'conn':
                    conn = value
                    conn.commit()
            

    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    

update_user_email(user_id=5, new_email='Crawford_Cartwright@hotmail.com')