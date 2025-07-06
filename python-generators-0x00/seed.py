import functools
import mysql.connector.errors as mysqlError
import mysql.connector.pooling
import csv
from dotenv import load_dotenv
import os

def exception_handler(func):
    """
    Decorator that wraps a function with a try/except block to handle common
    MySQL and Python exceptions. Raises the error after displaying it.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (mysqlError.PoolError, mysqlError.InterfaceError,
                mysqlError.InternalError, mysqlError.ProgrammingError,
                mysqlError.OperationalError, mysqlError.IntegrityError,
                mysqlError.DataError, mysqlError.NotSupportedError,
                mysqlError.Warning, ReferenceError, ValueError,
                AttributeError) as err:
            print(f"Error: {err}")
            raise
        except Exception as err:
            print(f"Error: {err}")
            raise
    return wrapper

def get_config_parameters(file=None):
    """
    Retrieves MySQL connection parameters from an environment file.
    If no file is provided, it defaults to 'secrets.env'.
    Returns:
        dict: A dictionary containing username, host, and password.
    """
    if file is None:
        file = 'secrets.env'

    load_dotenv(file)
    keys = ['username', 'host', 'password']
    values = [os.getenv('DB_USERNAME'), os.getenv('DB_HOST'), os.getenv('DB_PASSWORD')]
    return dict(zip(keys, values))

@exception_handler
def connect_db():
    """
    Establishes a connection to the MySQL server using connection pooling.
    Connection parameters are loaded from the .env file.
    Returns:
        mysql.connector.connection.MySQLConnection: A live connection object.
    """
    config = get_config_parameters()
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(**config)
    return connection_pool.get_connection()

@exception_handler
def create_database(connection=None):
    """
    Creates the database `ALx_prodev` if it does not exist.
    Confirms its creation by listing all databases and searching for it.
    Returns:
        bool: True if the database exists after creation.
    """
    if connection is None:
        connection = connect_db()

    sql_operation = """
        CREATE DATABASE IF NOT EXISTS ALx_prodev;
        SHOW DATABASES;
    """
    with connection.cursor() as create_cursor:
        create_cursor.execute(sql_operation)
        create_cursor.commit()
        while create_cursor.nextset():
            result_set = create_cursor.fetchall()
            for row in result_set:
                if row[0].lower() == 'alx_prodev':
                    return True

@exception_handler
def connect_to_prodev():
    """
    Connects to the `ALx_prodev` database and confirms selection.
    Returns:
        mysql.connector.connection.MySQLConnection: A connection to the selected database.
    """
    connection = connect_db()
    cursor = connection.cursor()

    queries = """
        USE alx_prodev;
        SELECT DATABASE();
    """
    cursor.execute(queries)
    while cursor.nextset():
        result = cursor.fetchone()
        if result:
            selected = result[0]
    return connection

@exception_handler
def create_table(connection=None):
    """
    Creates the `user_data` table in the `ALx_prodev` database if it doesn't exist.
    Also verifies its existence and displays its schema.
    """
    close_when_done = False
    if connection is None:
        connection = connect_to_prodev()
        close_when_done = True

    query = """ 
        CREATE TABLE IF NOT EXISTS user_data(
            user_id CHAR(36) PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL(3,0) NOT NULL
        );
        SHOW TABLES;
    """
    with connection.cursor() as insert_cursor:
        insert_cursor.execute(query)
        insert_cursor.commit()
        while insert_cursor.nextset():
            results = insert_cursor.fetchall()
            for row in results:
                if row[0].lower() == 'user_data':
                    insert_cursor.execute("DESCRIBE user_data;")
                    if insert_cursor.with_rows:
                        schema = (row for row in insert_cursor.fetchall())
                        for col in schema:
                            _ = (col[0], col[1])

    if close_when_done:
        connection.close()

@exception_handler
def get_csv_data(filepath, **kwargs):
    """
    Loads data from a CSV file and yields each row as a list.
    Skips the header row and reads using the default comma delimiter.
    Yields:
        list: A row of data from the CSV file.
    """
    with open(file=filepath, mode="r") as csv_file:
        csv_gencomp = csv.reader(csv_file, delimiter=",")
        next(csv_gencomp)
        for value in csv_gencomp:
            yield value

@exception_handler
def insert_data(connection=None, data=None):
    """
    Inserts data from a CSV file into the `user_data` table.
    Uses a generator to load the data and performs a batch insert.
    Commits changes and closes the connection afterward.
    """
    close_when_done = False
    if connection is None:
        connection = connect_to_prodev()
        close_when_done = True

    if data is None:
        raise ValueError("CSV file Must be Provided for Insertion!")

    generator_obj = get_csv_data(data, delimiter=",")
    data_batch = [tuple(row) for row in generator_obj]

    query = """
        INSERT INTO user_data(user_id, name, email, age)
        VALUES(%s, %s, %s, %s);
    """
    with connection.cursor() as insert_cursor:
        insert_cursor.executemany(query, data_batch)
        connection.commit()

    if close_when_done:
        connection.close()
    
    return True
