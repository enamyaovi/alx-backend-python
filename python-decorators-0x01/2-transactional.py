import sqlite3
import functools
import inspect

# Import from other module
with_db_connection_module = __import__('1-with_db_connection')
with_db_connection = with_db_connection_module.with_db_connection
error_logger = with_db_connection_module.error_logger


def transactional(func):
    """
    A decorator that wraps a DB operation in a transaction.
    Commits if all goes well, rolls back on failure.
    Logs any error using the error logger from with_db_connection.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        try:
            result = func(*args, **kwargs)

            # Look for 'conn' and commit if it's there
            for name, value in bound.arguments.items():
                if name == 'conn':
                    if isinstance(value, sqlite3.Connection):
                        value.commit()
            return result

        except (
            sqlite3.Error, sqlite3.Warning, sqlite3.InterfaceError,
            sqlite3.DatabaseError, sqlite3.DataError, sqlite3.IntegrityError,
            sqlite3.InternalError, sqlite3.NotSupportedError, Exception
        ) as e:
            # Roll back if 'conn' exists
            for name, value in bound.arguments.items():
                if name == 'conn':
                    if isinstance(value, sqlite3.Connection):
                        value.rollback()
                        error_logger.error(f"Transaction rolled back due to: {e}")
                        break
            else:
                error_logger.exception(f"Exception occurred with no DB rollback: {e}")

    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email in the database.
    Transaction is managed automatically.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage
if __name__ == "__main__":
    update_user_email(user_id=5, new_email="Crawford_Cartwright@hotmail.com")
