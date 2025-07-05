import seed

def paginate_users(page_size, offset):
    """
    A fxn that retrieves data from the db by pagesize and offset
    where page size is the limit of rows
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size:int):
    """
    A function that will only fetch the next page when needed at an offset of 0
    """
    if not isinstance(page_size, int):
        raise ValueError("Page Size must be an Integer")
    
    data = paginate_users(page_size, offset=0)

    
