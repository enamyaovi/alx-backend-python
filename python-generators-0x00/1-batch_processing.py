from seed import connect_to_prodev
from itertools import islice

def stream_users_in_batches(batch_size: int):
    """
    Generator function that streams user records from the database
    in batches of the specified size. Yields each user row as a dictionary.

    Args:
        batch_size (int): The number of rows to retrieve in a single batch.

    Yields:
        dict: A single user record from the batch.
    """
    if not isinstance(batch_size, int):
        raise ValueError(f"Sorry but '{batch_size}' is not a valid integer")

    connection = connect_to_prodev()
    stream_cursor = connection.cursor(dictionary=True)

    try:
        stream_cursor.execute("SELECT * FROM user_data;")
        result = stream_cursor.fetchmany(size=batch_size)
        for row in result:
            yield row
    except GeneratorExit:
        if stream_cursor.with_rows:
            _ = stream_cursor.fetchall()
        raise
    finally:
        stream_cursor.close()
        connection.close()


def batch_processing(batch_size: int):
    """
    Consumer function that processes a batch of user data streamed from
    the database. Filters and prints only users over the age of 25.

    Args:
        batch_size (int): The number of user records to retrieve and evaluate.
    """
    batch_data = stream_users_in_batches(batch_size)
    for user in islice(batch_data, batch_size):
        if user['age'] > 25:
            return print(user)
