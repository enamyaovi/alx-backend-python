from seed2 import connect_db


def stream_users_in_batches(batch_size:int):

    if not isinstance(batch_size, int):
        raise ValueError(f"Sorry but '{batch_size}' is not a valid integer")
    else:
        row_limit = batch_size

    select_database = """
            USE alx_prodev;
            """

    query = f"""
        SELECT * FROM user_data 
        LIMIT {row_limit};   
        """
    
    with connect_db() as connection:
    # connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(select_database)
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            output = {
            'user_id':row[0],
            'name':row[1],
            'email':row[2],
            'age':row[3]
        }
            yield output

def batch_processing(batch_size:int):
    value = batch_size
    gencomp = stream_users_in_batches(batch_size=value)
    batch_result = [row for row in gencomp]

    for value in batch_result:
        if value['age'] > 25:
            print(value)
        
    