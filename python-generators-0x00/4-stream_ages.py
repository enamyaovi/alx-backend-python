from seed import connect_to_prodev

def stream_user_ages():
    """
    Generator function that streams user ages one by one
    from the user_data table in the database.
    Yields:
        dict: A dictionary with 'age' as key.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT age FROM user_data;")
        for row in cursor:
            yield row
    finally:
        cursor.close()
        connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using a memory-efficient generator.
    Uses enumerate to track count while summing user ages.
    Prints:
        Average age of users: average
    """
    total_age = 0
    count = 0

    for index, row in enumerate(stream_user_ages(), start=1):
        total_age += row['age']
        count = index  # last index = total number of users

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")