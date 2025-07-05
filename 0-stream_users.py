
from seed2 import connect_db

def stream_users():
    connection = connect_db()
    cursor = connection.cursor()

    select_database = """
                USE alx_prodev;
                """

    query = """
            SELECT * FROM user_data;
            """
    
    cursor.execute(select_database)
    cursor.execute(query)

    result = cursor.fetchall()
    for row in result:
        output = {
            'user_id':row[0],
            'name':row[1],
            'email':row[2],
            'age':row[3]
        }
        yield output
    
    cursor.close()
    connection.close()
    