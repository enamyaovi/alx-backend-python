#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error as MySQL_Error # import my sql Error class 
from dotenv import load_dotenv
import os
from functools import wraps

# Load environment variables
load_dotenv()

# Retrieve them
db_user = os.getenv('USERNAME')
db_host = os.getenv('HOST_IP')
db_password = os.getenv('PASSWORD')

# print("Retrieved values:", username, host, password)
config = {
    'user': db_user,
    'host': db_host,
    'password': db_password
}

# For future use
database_details = {
    'database_name': 'ALX_prodev',
    'table_name': 'user_data'
}


import functools
def handle_db_errors(func):
    """
    
    """
    @functools.wraps(func)
    def wrapper_handle_errors(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return func(*args, **kwargs)
        except MySQL_Error.OperationalError as e:
            print('For some reason your database cannot connect')
            print(f"Details: {e}")
        except MySQL_Error.ProgrammingError as e:
            # Raised if there is a syntax error in the SQL query
            print("Programming error: Issue with SQL syntax.")
            print(f"Details: {e}")
        except MySQL_Error.DatabaseError as e:
            # Raised for issues related to the database connection or operation
            print("Database error: Problem occurred while creating the database.")
            print(f"Details: {e}")
        except MySQL_Error.IntegrityError as e:
            # Raised when data violates integrity constraints (e.g., duplicate entries, foreign key issues)
            print("Integrity error: Data conflicts with existing constraints.")
            print(f"Details: {e}")
        except Exception as e:
            print('Error')
            print(f"General Error, {e}")

    return wrapper_handle_errors

@handle_db_errors
def connect_db(*args, username=db_user,host=db_host,password=db_password, **kwargs):
    print('ready to establish connection')
    return mysql.connector.connect()
    

@handle_db_errors
def create_database(*args, **kwargs):
    return mysql.connector.connect(*args, **kwargs)