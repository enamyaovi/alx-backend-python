from seed import exception_handler, connect_to_prodev

@exception_handler
def stream_users():
    """
    Generator to stream user_data rows one by one.
    Handles unread results if the generator is closed early.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
    except GeneratorExit:
        # Clean unread results before generator is finalized
        if cursor.with_rows:
            _ = cursor.fetchall()
        raise  
    finally:
        cursor.close()
        connection.close()