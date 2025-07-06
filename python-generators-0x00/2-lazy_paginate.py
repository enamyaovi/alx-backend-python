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

@seed.exception_handler
def lazy_paginate(page_size: int):
    """
    Generator that lazily paginates users from the database.

    This function yields batches of users retrieved from the `user_data` table 
    using the given page size. It fetches the next page only when needed, 
    starting at offset 0 and continuing until no more rows are returned.

    Args:
        page_size (int): The number of rows to include per page.

    Yields:
        list[dict]: A batch (page) of user records as dictionaries.

    Raises:
        ValueError: If the page_size is not an integer.
    """
    if not isinstance(page_size, int):
        raise ValueError("Page size must be an integer.")

    page_index = 0  # Starts at offset 0

    while True:
        offset = page_size * page_index
        next_page = paginate_users(page_size, offset=offset)
        if not next_page:
            break
        yield next_page
        page_index += 1
