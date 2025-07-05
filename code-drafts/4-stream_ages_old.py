from seed2 import connect_to_prodev


def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor()

    select_database = """
                USE alx_prodev;
                """

    query = """
            SELECT age FROM user_data;
            """
    
    cursor.execute(select_database)
    cursor.execute(query)

    result = cursor.fetchall()
    for row in result:
        yield row[0]
    

def calculate_average_age():
    total = sum(age for age in stream_user_ages())
    enum = list(enumerate(stream_user_ages(), start=1))
    count = enum[-1][0]
    
    average_age = total/count

    statement = f"Average age of users: {average_age}"

    return statement