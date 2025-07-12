"""
create a class based context manager to handle opening and closing database connections automatically
"""
import mysql
import mysql.connector
from utility import seed

#get configuration parameters
get_config = seed.get_config_parameters('db_secrets.env')

class DatabaseConnection:
    def __init__(self, config:dict=get_config, db_name=None):
        if not db_name:
            if not config['database']:
                raise ValueError("No database provided to connect to")
        else:
            config['database'] = db_name
        
        self.config = config
        self.connection = None
        
    @seed.exception_handler
    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        return self.connection

    @seed.exception_handler
    def __exit__(self, type, value, traceback):
        if type is None:
            self.connection.commit() # type: ignore
        else:
            self.connection.rollback() #type: ignore
        self.connection.close() #type: ignore
        return False

def main():
    with DatabaseConnection(db_name='alx_prodev') as cnx:
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM users LIMIT 5")
        return cursor.fetchall()
    

if __name__ == "__main__":
    data = main()
    for user in data:
        print(user)

