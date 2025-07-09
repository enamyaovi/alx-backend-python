import sqlite3 
import functools, inspect

def with_db_connection(func):
    """ your code goes here""" 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        conn = sqlite3.connect('users.db')

        #inspect the signature of the function and retrieve the args passed
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        try:
            #loop through the arguments then check for connection parameter
            
            #type check the parameter to enforce they are the right type
            #don't even need this in the assignment line 20-28
            for name, value in bound.arguments.items():
                if name == 'conn':
                    if not isinstance(value, sqlite3.Connection):
                        raise TypeError
                    else:
                        return func(*args, **kwargs)
                if name == 'user_id':
                    if not isinstance(value,int):
                        raise TypeError

            #if no such parameter is provided create a connection ourselves
            if not 'conn' in bound.arguments.items():
                return func(conn, *args, **kwargs)
            
        #if cnx then connect to database using that connection
        except Exception:
            print("Error")
        else:
            print("function call")
            # return func(conn, *args, **kwargs)
    return wrapper
        

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 
# user = get_user_by_id(user_id=1)
# print(user)