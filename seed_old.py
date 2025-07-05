import mysql.connector
import mysql.connector.errors as mysqlError
import functools
from dotenv import load_dotenv
import os
import csv

def exception_handler(func):
    """
    a decorator that handles exceptions for SQL-Python connector methods
    """
    #defining inner wrapper
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print('Trying to accomplish Task')
            result = func(*args, **kwargs)
        except mysqlError.IntegrityError as e:
            print(f"{e}")
        except mysqlError.OperationalError as e:
            print(f"{e}")
        except mysqlError.DatabaseError as e:
            print(f"{e}")
        except mysqlError.InterfaceError as e:
            print(f"{e}")
        except mysqlError.Warning as e:
            print(f"{e}")
        except Exception as e:
            print('Some exception was raised when trying')
            print(f"{e}")
            return None
        else:
            print('Task was completed no errors caught')
            return result
    return wrapper

@exception_handler
def get_csv_data(filename, **kwargs):
    with open(file=filename, mode="r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        next(csv_reader)
        for value in csv_reader:
            yield value

def get_config_params():
    load_dotenv()
    config = {
        'username':os.getenv('DB_USERNAME'),
        'host':os.getenv('DB_HOST'),
        'password':os.getenv('DB_PASSWORD'),
    }
    return config

@exception_handler
def connect_db():
    """
    Attempts to connect to an SQL database
    """
    param = get_config_params()
    connection = mysql.connector.connect(**param)
    return connection

@exception_handler
def create_database(*args, connection=None,**kwargs):
    if connection is None:
        connection = connect_db()
    mycursor = connection.cursor()
    # creating a database
    mycursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    mycursor.execute("SHOW DATABASES;")
    rows = mycursor.fetchall()
    result = [x for x in rows if x[0].lower() == 'alx_prodev']
    outcome =print(f"You have successfully created Database: {result[0][0]}")
    return outcome

@exception_handler
def connect_to_prodev(*args,db_name=None,connection=None, **kwargs):
    """
    
    """
    if db_name is None:
        db_name = 'alx_prodev'
    if connection is None:
        connection = connect_db()
        mycursor = connection.cursor()
    
    #selecting the database
    mycursor.execute(f"USE {db_name};")
    mycursor.execute(f"SELECT DATABASE();")
    rows = mycursor.fetchone()
    print(f"You are currently using database: {rows[0]}")


    connection = connect_db()
    return connection

@exception_handler
def create_table(*args, connection=None, **kwargs):
    if connection is None:
        connection = connect_db()
        create_cursor = connection.cursor()

    create_cursor.execute("""
        USE alx_prodev;
        """)
    
    create_cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data(
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(70) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL NOT NULL
            );
        """)
    
    create_cursor.execute("""
        SHOW TABLES;
        """)

    rows = create_cursor.fetchall()

    [print(f"Table: {x[0]} created") if x[0].lower()=='user_data' else print("Table: user_data does not exist") for x in rows]

    return None


@exception_handler
def insert_data(*args, connection=None, file=None, **kwargs):

    if connection is None:
        connection = connect_db()
    insert_cursor = connection.cursor()

    if file is None:
        file = 'users_data.csv'
    gencomp = get_csv_data(filename=file)
    
        
    data_batch = [tuple(row) for row in gencomp]
    

    select_database_query = """
                USE alx_prodev;
                        """
    
    insert_query = """
            INSERT INTO user_data(user_id, name, email, age)
            VALUES(%s, %s, %s, %s);"""
    
    insert_cursor.execute(select_database_query)
    insert_cursor.executemany(insert_query,data_batch)
    connection.commit()
    insert_cursor.close()
    connection.close()

    return None