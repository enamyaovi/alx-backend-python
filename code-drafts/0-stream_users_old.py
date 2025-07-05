
from seed import connect_to_prodev

def stream_users():
    connection = connect_to_prodev()

    query = """
            SELECT * FROM user_data;
            """
    
    with connection.cursor() as cursor:    
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

    connection.close()
    