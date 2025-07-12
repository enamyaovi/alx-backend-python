import sqlite3
import functools
import inspect

with_db_connection = __import__('1-with_db_connection').with_db_connection

# Decorator to wrap a function in a database transaction
def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        try:
            result = func(*args, **kwargs)
            # Commit transaction on success
            for name, value in bound.arguments.items():
                if name == 'conn':
                    value.commit()
            print("Transaction committed")
            return result

        except (sqlite3.Error, sqlite3.Warning, sqlite3.InterfaceError,
                sqlite3.DatabaseError, sqlite3.DataError,
                sqlite3.IntegrityError, sqlite3.InternalError,
                sqlite3.NotSupportedError, Exception) as e:
            # Rollback transaction on failure
            for name, value in bound.arguments.items():
                if name == 'conn':
                    value.rollback()
            print(f"Transaction rolled back due to error: {e}")

    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage
update_user_email(user_id=5, new_email='Crawford_Cartwright@hotmail.com')
